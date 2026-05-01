"""
用户中心工具
用户信息、收货地址、优惠券管理
"""
import json
import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime
from langchain.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context

# 用户数据存储
users_db: Dict[str, Dict[str, Any]] = {}

# 收货地址存储
addresses_db: Dict[str, List[Dict[str, Any]]] = {}


@tool
def get_user_profile(user_id: str) -> str:
    """
    获取用户信息
    
    Args:
        user_id: 用户ID
        
    Returns:
        用户信息JSON
    """
    ctx = request_context.get() or new_context(method="get_user_profile")
    
    user = users_db.get(user_id)
    if not user:
        # 创建新用户
        user = {
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "tier": "BRONZE",
            "points": 0,
            "language": "en",
        }
        users_db[user_id] = user
    
    return json.dumps({
        "success": True,
        "user": user
    })


@tool
def update_user_profile(
    user_id: str,
    name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    language: Optional[str] = None
) -> str:
    """
    更新用户信息
    
    Args:
        user_id: 用户ID
        name: 姓名(可选)
        email: 邮箱(可选)
        phone: 电话(可选)
        language: 语言偏好(可选)
        
    Returns:
        更新结果JSON
    """
    ctx = request_context.get() or new_context(method="update_user_profile")
    
    user = users_db.get(user_id)
    if not user:
        user = {
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "tier": "BRONZE",
            "points": 0,
        }
        users_db[user_id] = user
    
    if name:
        user["name"] = name
    if email:
        user["email"] = email
    if phone:
        user["phone"] = phone
    if language:
        user["language"] = language
    
    user["updated_at"] = datetime.utcnow().isoformat()
    
    return json.dumps({
        "success": True,
        "user": user
    })


@tool
def add_shipping_address(
    user_id: str,
    name: str,
    phone: str,
    province: str,
    city: str,
    address: str,
    postal_code: str,
    is_default: bool = False
) -> str:
    """
    添加收货地址
    
    Args:
        user_id: 用户ID
        name: 收货人姓名
        phone: 联系电话
        province: 省份
        city: 城市
        address: 详细地址
        postal_code: 邮政编码
        is_default: 是否设为默认地址
        
    Returns:
        添加结果JSON
    """
    ctx = request_context.get() or new_context(method="add_shipping_address")
    
    if user_id not in addresses_db:
        addresses_db[user_id] = []
    
    address_id = f"ADDR{uuid.uuid4().hex[:8].upper()}"
    
    new_address = {
        "address_id": address_id,
        "name": name,
        "phone": phone,
        "province": province,
        "city": city,
        "address": address,
        "postal_code": postal_code,
        "is_default": is_default,
    }
    
    # 如果设为默认，先取消其他默认
    if is_default:
        for addr in addresses_db[user_id]:
            addr["is_default"] = False
    
    addresses_db[user_id].append(new_address)
    
    return json.dumps({
        "success": True,
        "address": new_address
    })


@tool
def get_shipping_addresses(user_id: str) -> str:
    """
    获取用户收货地址列表
    
    Args:
        user_id: 用户ID
        
    Returns:
        地址列表JSON
    """
    addresses = addresses_db.get(user_id, [])
    
    return json.dumps({
        "success": True,
        "count": len(addresses),
        "addresses": addresses
    })


@tool
def delete_shipping_address(user_id: str, address_id: str) -> str:
    """
    删除收货地址
    
    Args:
        user_id: 用户ID
        address_id: 地址ID
        
    Returns:
        操作结果JSON
    """
    if user_id not in addresses_db:
        return json.dumps({
            "success": False,
            "error": "No addresses found"
        })
    
    original_count = len(addresses_db[user_id])
    addresses_db[user_id] = [a for a in addresses_db[user_id] if a["address_id"] != address_id]
    
    if len(addresses_db[user_id]) == original_count:
        return json.dumps({
            "success": False,
            "error": "Address not found"
        })
    
    return json.dumps({
        "success": True,
        "message": "Address deleted"
    })
