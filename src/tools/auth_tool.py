"""
用户认证工具
"""
import json
import re
import uuid
from datetime import datetime
from langchain.tools import tool
from storage.database.supabase_client import get_supabase_client
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context


# 南非手机号验证
PHONE_PATTERN = re.compile(r'^\+?27[1-9][0-9]{8}$')

# 邮箱验证
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# 模拟验证码存储
VERIFICATION_CODES = {}


def _validate_phone(phone: str) -> bool:
    return bool(PHONE_PATTERN.match(phone.replace(' ', '')))


def _validate_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.match(email))


def _generate_user_id() -> int:
    return int(datetime.utcnow().timestamp() * 1000) % 1000000


def _generate_code() -> str:
    return str(uuid.uuid4().hex[:6]).upper()


def _format_zar(cents: int) -> str:
    return f"R{cents/100:.2f}"


@tool
def send_verification_code(identifier: str, type: str = "register") -> str:
    """
    发送验证码
    
    Args:
        identifier: 手机号或邮箱
        type: 类型 (register/login)
        
    Returns:
        发送结果JSON
    """
    ctx = request_context.get() or new_context(method="send_verification_code")
    
    identifier = identifier.strip()
    is_phone = identifier.startswith('+') or identifier.startswith('0')
    
    if is_phone:
        if not _validate_phone(identifier):
            return json.dumps({"success": False, "error": "Invalid SA phone number"})
    else:
        if not _validate_email(identifier):
            return json.dumps({"success": False, "error": "Invalid email format"})
    
    code = _generate_code()
    VERIFICATION_CODES[identifier] = {
        'code': code,
        'type': type,
        'created_at': datetime.utcnow().isoformat(),
        'expires_at': datetime.utcnow().isoformat()
    }
    
    return json.dumps({
        "success": True,
        "message": f"Verification code sent to {identifier}",
        "code": code,
        "expires_in": 300
    })


@tool
def verify_code_and_login(identifier: str, code: str) -> str:
    """
    验证并登录
    
    Args:
        identifier: 手机号或邮箱
        code: 验证码
        
    Returns:
        登录结果JSON
    """
    ctx = request_context.get() or new_context(method="verify_code_and_login")
    
    stored = VERIFICATION_CODES.get(identifier)
    if not stored or stored['code'] != code.upper():
        return json.dumps({"success": False, "error": "Invalid verification code"})
    
    client = get_supabase_client()
    field = 'phone' if '+' in identifier else 'email'
    
    user = client.table('users').select('*').eq(field, identifier).execute()
    
    if user.data:
        user_data = user.data[0]
    else:
        user_id = _generate_user_id()
        user_data = {
            'id': user_id,
            'phone': identifier if '+' in identifier else None,
            'email': identifier if '@' in identifier else None,
            'created_at': datetime.utcnow().isoformat(),
            'tier': 'BRONZE',
            'points': 0
        }
        client.table('users').insert(user_data).execute()
    
    return json.dumps({
        "success": True,
        "message": "Login successful",
        "user": user_data
    })


@tool
def register_user(phone: str = None, email: str = None, name: str = None) -> str:
    """
    注册用户
    
    Args:
        phone: 手机号
        email: 邮箱
        name: 姓名
        
    Returns:
        注册结果JSON
    """
    ctx = request_context.get() or new_context(method="register_user")
    
    if not phone and not email:
        return json.dumps({"success": False, "error": "Phone or email required"})
    
    client = get_supabase_client()
    
    if phone:
        phone = phone.strip()
        if not _validate_phone(phone):
            return json.dumps({"success": False, "error": "Invalid phone number"})
        existing = client.table('users').select('id').eq('phone', phone).execute()
        if existing.data:
            return json.dumps({"success": False, "error": "Phone already registered"})
    
    if email:
        email = email.strip()
        if not _validate_email(email):
            return json.dumps({"success": False, "error": "Invalid email"})
        existing = client.table('users').select('id').eq('email', email).execute()
        if existing.data:
            return json.dumps({"success": False, "error": "Email already registered"})
    
    user_id = _generate_user_id()
    user_data = {
        'id': user_id,
        'phone': phone,
        'email': email,
        'name': name,
        'created_at': datetime.utcnow().isoformat(),
        'tier': 'BRONZE',
        'points': 100,
        'language': 'en'
    }
    client.table('users').insert(user_data).execute()
    
    return json.dumps({
        "success": True,
        "message": "Registration successful",
        "user": user_data
    })


@tool
def get_current_user(identifier: str) -> str:
    """
    获取当前用户信息
    
    Args:
        identifier: 手机号或邮箱
        
    Returns:
        用户信息JSON
    """
    ctx = request_context.get() or new_context(method="get_current_user")
    
    client = get_supabase_client()
    field = 'phone' if '+' in identifier else 'email'
    
    user = client.table('users').select('*').eq(field, identifier).execute()
    
    if not user.data:
        return json.dumps({"success": False, "error": "User not found"})
    
    return json.dumps({"success": True, "user": user.data[0]})
