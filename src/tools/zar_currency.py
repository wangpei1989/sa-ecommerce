"""
南非本地化工具
货币转换、语言切换、南非省份数据
"""
import json
from typing import Optional
from langchain.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context

# 南非兰特 (ZAR) 汇率 (示例，实际应调用实时API)
ZAR_EXCHANGE_RATES = {
    "USD": 18.50,   # 1 USD = 18.50 ZAR
    "EUR": 20.10,   # 1 EUR = 20.10 ZAR
    "GBP": 23.50,   # 1 GBP = 23.50 ZAR
    "CNY": 2.55,    # 1 CNY = 2.55 ZAR
}

# 南非官方语言
SOUTH_AFRICA_LANGUAGES = {
    "en": "English",
    "zu": "isiZulu (祖鲁语)",
    "af": "Afrikaans (阿非利堪斯语)",
    "xh": "isiXhosa (科萨语)",
    "st": "Sesotho (索托语)",
    "tn": "Setswana (茨瓦纳语)",
}

# 南非省份
SOUTH_AFRICA_PROVINCES = {
    "EC": "Eastern Cape",
    "FS": "Free State",
    "GP": "Gauteng",
    "KZN": "KwaZulu-Natal",
    "LP": "Limpopo",
    "MP": "Mpumalanga",
    "NC": "Northern Cape",
    "NW": "North West",
    "WC": "Western Cape",
}


@tool
def convert_to_zar(amount: float, from_currency: str) -> str:
    """
    货币转换为南非兰特
    
    Args:
        amount: 金额
        from_currency: 源货币代码 (USD/EUR/GBP/CNY)
        
    Returns:
        转换结果JSON (金额单位: 分/cent)
    """
    ctx = request_context.get() or new_context(method="convert_to_zar")
    
    from_currency = from_currency.upper()
    if from_currency == "ZAR":
        return json.dumps({
            "success": True,
            "original_amount": amount,
            "original_currency": "ZAR",
            "zar_amount": amount,
            "zar_amount_cents": int(amount * 100),
            "display": f"R{amount:.2f}"
        })
    
    rate = ZAR_EXCHANGE_RATES.get(from_currency)
    if not rate:
        return json.dumps({
            "success": False,
            "error": f"Unsupported currency: {from_currency}",
            "supported_currencies": list(ZAR_EXCHANGE_RATES.keys()) + ["ZAR"]
        })
    
    zar_amount = amount * rate
    zar_cents = int(zar_amount * 100)
    
    return json.dumps({
        "success": True,
        "original_amount": amount,
        "original_currency": from_currency,
        "exchange_rate": rate,
        "zar_amount": round(zar_amount, 2),
        "zar_amount_cents": zar_cents,
        "display": f"R{zar_amount:.2f}"
    })


@tool
def format_zar_price(amount_cents: int, show_symbol: bool = True) -> str:
    """
    格式化南非兰特价格显示
    
    Args:
        amount_cents: 金额(单位: 分)
        show_symbol: 是否显示货币符号
        
    Returns:
        格式化后的价格字符串
    """
    amount = amount_cents / 100
    
    if show_symbol:
        return f"R{amount:,.2f}"
    return f"{amount:,.2f}"


@tool
def get_supported_languages() -> str:
    """
    获取支持的南非官方语言列表
    
    Returns:
        语言列表JSON
    """
    return json.dumps({
        "success": True,
        "languages": SOUTH_AFRICA_LANGUAGES,
        "default": "en"
    })


@tool
def get_provinces() -> str:
    """
    获取南非九省列表
    
    Returns:
        省份列表JSON
    """
    return json.dumps({
        "success": True,
        "provinces": SOUTH_AFRICA_PROVINCES
    })


@tool
def validate_sa_phone(phone: str) -> str:
    """
    验证南非手机号码格式
    
    南非手机号格式: +27 开头，10位数字
    
    Args:
        phone: 手机号码
        
    Returns:
        验证结果JSON
    """
    import re
    
    # 清理号码
    clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # 验证格式
    patterns = [
        r'^\+27[6-9]\d{8}$',           # +27 6x/7x/8x/9x xxxxxxxx
        r'^0[6-9]\d{8}$',               # 06x/07x/08x/09x xxxxxxxx
    ]
    
    is_valid = any(re.match(p, clean_phone) for p in patterns)
    
    return json.dumps({
        "success": True,
        "original": phone,
        "normalized": clean_phone,
        "is_valid": is_valid,
        "message": "Valid South African phone number" if is_valid else "Invalid format"
    })


@tool
def validate_postal_code(postal_code: str, province: Optional[str] = None) -> str:
    """
    验证南非邮政编码
    
    Args:
        postal_code: 邮编
        province: 省份(可选，用于验证范围)
        
    Returns:
        验证结果JSON
    """
    import re
    
    clean_code = re.sub(r'[\s\-]', '', postal_code)
    
    # 南非邮编为4位数字
    is_valid = bool(re.match(r'^\d{4}$', clean_code))
    
    return json.dumps({
        "success": True,
        "original": postal_code,
        "cleaned": clean_code,
        "is_valid": is_valid,
        "message": "Valid postal code" if is_valid else "Must be 4 digits"
    })
