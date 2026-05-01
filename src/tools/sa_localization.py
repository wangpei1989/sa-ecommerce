"""
南非本地化适配工具集
包含：货币转换、多语言支持、省份城市数据、验证规则、弱网适配
"""
import json
import re
from datetime import datetime
from typing import Optional
from langchain.tools import tool

# ==================== ZAR货币转换模块 ====================

# 汇率数据（基于2024年参考汇率）
EXCHANGE_RATES = {
    "ZAR": 1.0,           # 南非兰特基准
    "USD": 0.054,         # 美元
    "EUR": 0.050,         # 欧元
    "GBP": 0.043,         # 英镑
    "CNY": 0.39,          # 人民币
    "INR": 4.52,          # 印度卢比
    "BRL": 0.27,          # 巴西雷亚尔
    "AUD": 0.083,         # 澳大利亚元
}

def cents_to_zar(cents: int) -> str:
    """分转ZAR格式（南非当地货币显示）"""
    amount = cents / 100
    return f"R{amount:,.2f}"

def convert_currency(amount: float, from_currency: str, to_currency: str = "ZAR") -> float:
    """货币转换"""
    from_curr = from_currency.upper()
    to_curr = to_currency.upper()
    
    if from_curr not in EXCHANGE_RATES or to_curr not in EXCHANGE_RATES:
        return amount
    
    # 先转ZAR，再转目标货币
    zar_amount = amount / EXCHANGE_RATES[from_curr]
    return zar_amount * EXCHANGE_RATES[to_curr]

@tool
def convert_to_zar(amount: float, currency: str) -> str:
    """
    将任意货币转换为南非兰特(ZAR)
    
    参数:
        amount: 金额
        currency: 货币代码 (USD/EUR/GBP/CNY/INR等)
    
    返回:
        ZAR格式金额字符串
    """
    zar_amount = convert_currency(amount, currency, "ZAR")
    return json.dumps({
        "success": True,
        "original": f"{amount} {currency}",
        "zar_amount": f"R{zar_amount:,.2f}",
        "zar_cents": int(zar_amount * 100)
    })

@tool
def convert_from_zar(amount: float, target_currency: str) -> str:
    """
    将南非兰特(ZAR)转换为其他货币
    
    参数:
        amount: ZAR金额
        target_currency: 目标货币代码 (USD/EUR/GBP等)
    
    返回:
        转换后的金额字符串
    """
    converted = convert_currency(amount, "ZAR", target_currency)
    return json.dumps({
        "success": True,
        "zar_amount": f"R{amount:,.2f}",
        "converted_amount": f"{converted:,.2f} {target_currency}"
    })

@tool
def get_exchange_rates() -> str:
    """获取当前汇率列表（以ZAR为基准）"""
    rates = [{"currency": c, "rate": r} for c, r in EXCHANGE_RATES.items()]
    return json.dumps({
        "success": True,
        "base": "ZAR",
        "rates": rates,
        "updated_at": datetime.now().isoformat()
    })

# ==================== 多语言支持模块 ====================

# 南非11种官方语言
LANGUAGES = {
    "en": "English",
    "af": "Afrikaans",           # 阿非利卡语
    "zu": "Zulu",                # 祖鲁语
    "xh": "Xhosa",               # 科萨语
    "nso": "Northern Sotho",      # 北索托语
    "st": "Southern Sotho",      # 南索托语
    "tn": "Tswana",              # 茨瓦纳语
    "ve": "Venda",               # 文达语
    "ts": "Tsonga",              # 聪加语
    "ss": "Swati",               # 斯威士语
    "tn": "Tswana",              # 茨瓦纳语
}

# 多语言翻译词库
TRANSLATIONS = {
    "product": {
        "en": "Product", "af": "Produk", "zu": "I-Product", "xh": "Imveliso",
        "nso": "Thoto", "st": "Mohlolo", "tn": "Tlhago", "ve": "M户口",
        "ts": "Xikombelo", "ss": "Luhlelo"
    },
    "cart": {
        "en": "Shopping Cart", "af": "Stropmandjie", "zu": "Indwangu yokuthenga",
        "xh": "Isitya sokuthenga", "nso": "Koli ya go reka", "st": "Koloi ea ho reka",
        "tn": "mogalabagolo", "ve": "kha dzo", "ts": "xikombelo", "ss": "lithubuhlele"
    },
    "checkout": {
        "en": "Checkout", "af": "Kassa", "zu": "Ukuhlambela", "xh": "Ukuhlawula",
        "nso": "Go lefela", "st": "Ho lesa", "tn": "Go duelwa", "ve": "U dzhenelela",
        "ts": "ku lulamisa", "ss": "kuhambela"
    },
    "order": {
        "en": "Order", "af": "Bestelling", "zu": "I-oda", "xh": "Umyalelo",
        "nso": "Tae", "st": "Odara", "tn": "Taolo", "ve": "Mura",
        "ts": "Holobye", "ss": "Sitolo"
    },
    "payment": {
        "en": "Payment", "af": "Betaling", "zu": "Ukukhokha", "xh": "Intlawulo",
        "nso": "Teo", "st": "Tefo", "tn": "Teifo", "ve": "Mbulungeni",
        "ts": "mpfhumba", "ss": "kuhlobula"
    },
    "total": {
        "en": "Total", "af": "Totaal", "zu": "Ingxenye", "xh": "Zizonke",
        "nso": "Kapitlana", "st": "Kaofelang", "tn": "Kakaretso", "ve": "Mbulungeni",
        "ts": "N'wevano", "ss": "Kusize"
    },
    "shipping": {
        "en": "Shipping", "af": "Versending", "zu": "Ukuthunyelwa", "xh": "Ukuthunyelwa",
        "nso": "Peeletso", "st": "Ho romela", "tn": "Go romelwa", "ve": "U itwa",
        "ts": "ku sendzika", "ss": "kuhlambela"
    },
    "delivered": {
        "en": "Delivered", "af": "Gelewer", "zu": "Kufike", "xh": "Ifike",
        "nso": "Fetotse", "st": "Fihlometse", "tn": "E fitilwe", "ve": "A vhawe",
        "ts": "ku fika", "ss": "kufika"
    },
    "processing": {
        "en": "Processing", "af": "Verwerking", "zu": "Iqhuba", "xh": "Iqhube",
        "nso": "O tswalang", "st": "Ho sebetsa", "tn": "Go dirwa", "ve": "U shanda",
        "ts": "kuakiwa", "ss": "kuhlambela"
    },
    "cancelled": {
        "en": "Cancelled", "af": "Gekanselleer", "zu": "Khanseliwe", "xh": "Kanseliwe",
        "nso": "Gansitwwe", "st": "Ho hanoa", "tn": "Go nyelediwa", "ve": "A vha siwi",
        "ts": "ku khanceliwa", "ss": "kukhanselwa"
    },
}

@tool
def get_supported_languages() -> str:
    """获取支持的语言列表"""
    return json.dumps({
        "success": True,
        "languages": [
            {"code": "en", "name": "English", "native": "English"},
            {"code": "af", "name": "Afrikaans", "native": "Afrikaans"},
            {"code": "zu", "name": "Zulu", "native": "isiZulu"},
            {"code": "xh", "name": "Xhosa", "native": "isiXhosa"},
            {"code": "nso", "name": "Northern Sotho", "native": "Sesotho sa Leboa"},
            {"code": "st", "name": "Southern Sotho", "native": "Sesotho"},
            {"code": "tn", "name": "Tswana", "native": "Setswana"},
            {"code": "ve", "name": "Venda", "native": "Tshiven\u1d3a"},
            {"code": "ts", "name": "Tsonga", "native": "Xitsonga"},
            {"code": "ss", "name": "Swati", "native": "SiSwati"},
        ]
    })

@tool
def translate(keyword: str, source_lang: str = "en", target_lang: str = "zu") -> str:
    """
    翻译关键词到指定语言
    
    参数:
        keyword: 要翻译的关键词
        source_lang: 源语言代码
        target_lang: 目标语言代码
    
    返回:
        翻译后的文本
    """
    key_lower = keyword.lower()
    
    if key_lower in TRANSLATIONS:
        translations = TRANSLATIONS[key_lower]
        if target_lang in translations:
            return json.dumps({
                "success": True,
                "original": keyword,
                "translated": translations[target_lang],
                "source_lang": source_lang,
                "target_lang": target_lang
            })
    
    # 未找到翻译，返回原文
    return json.dumps({
        "success": True,
        "original": keyword,
        "translated": keyword,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "note": "Translation not available"
    })

@tool
def format_currency_zar(cents: int, locale: str = "en") -> str:
    """
    按南非本地化格式显示货币
    
    参数:
        cents: 金额（分）
        locale: 区域设置 (en/af/zu等)
    
    返回:
        格式化的货币字符串
    """
    amount = cents / 100
    
    # 不同语言的货币格式
    formats = {
        "en": f"R{amount:,.2f}",           # R1,234.56
        "af": f"R{amount:,.2f}",           # R1 234,56
        "zu": f"IR{amount:,.2f}",          # IR1,234.56 (Zulu uses IR)
        "xh": f"IR{amount:,.2f}",           # IR1,234.56
    }
    
    return json.dumps({
        "success": True,
        "cents": cents,
        "formatted": formats.get(locale, formats["en"]),
        "currency": "ZAR",
        "locale": locale
    })

# ==================== 南非省份/城市数据 ====================

PROVINCES_CITIES = {
    "GP": {
        "name": "Gauteng",
        "name_af": "Gauteng",
        "name_zu": "iGauteng",
        "capital": "Johannesburg",
        "cities": [
            {"name": "Johannesburg", "postal_codes": ["2000-2099"], "lat": -26.2041, "lon": 28.0473},
            {"name": "Pretoria", "postal_codes": ["0001-0199"], "lat": -25.7461, "lon": 28.1881},
            {"name": "Soweto", "postal_codes": ["1800-1899"], "lat": -26.2379, "lon": 27.8586},
            {"name": "Centurion", "postal_codes": ["0046-0157"], "lat": -25.8589, "lon": 28.1858},
            {"name": "Sandton", "postal_codes": ["2031-2196"], "lat": -26.0535, "lon": 28.0569},
        ]
    },
    "WC": {
        "name": "Western Cape",
        "name_af": "Wes-Kaap",
        "name_zu": "iNtshona Koloni",
        "capital": "Cape Town",
        "cities": [
            {"name": "Cape Town", "postal_codes": ["8000-8099"], "lat": -33.9249, "lon": 18.4241},
            {"name": "Stellenbosch", "postal_codes": ["7599-7735"], "lat": -33.9321, "lon": 18.8602},
            {"name": "Paarl", "postal_codes": ["7646-7680"], "lat": -33.7167, "lon": 18.9667},
            {"name": "George", "postal_codes": ["6529-6530"], "lat": -33.9681, "lon": 22.4617},
            {"name": "Worcester", "postal_codes": ["6845-6850"], "lat": -33.6500, "lon": 19.4500},
        ]
    },
    "KZN": {
        "name": "KwaZulu-Natal",
        "name_af": "KwaZulu-Natal",
        "name_zu": "iKwaZulu-Natali",
        "capital": "Pietermaritzburg",
        "cities": [
            {"name": "Durban", "postal_codes": ["4000-4099"], "lat": -29.8587, "lon": 31.0218},
            {"name": "Pietermaritzburg", "postal_codes": ["3200-3299"], "lat": -29.6000, "lon": 30.3833},
            {"name": "Richards Bay", "postal_codes": ["3900-3901"], "lat": -28.7830, "lon": 32.0377},
            {"name": "Ballito", "postal_codes": ["4399-4424"], "lat": -29.5333, "lon": 31.2333},
            {"name": "Ushaka", "postal_codes": ["4001-4004"], "lat": -29.8769, "lon": 31.0469},
        ]
    },
    "EC": {
        "name": "Eastern Cape",
        "name_af": "Oos-Kaap",
        "name_zu": "iMpuma Koloni",
        "capital": "Bhisho",
        "cities": [
            {"name": "Port Elizabeth", "postal_codes": ["6000-6071"], "lat": -33.9608, "lon": 25.6142},
            {"name": "East London", "postal_codes": ["5200-5299"], "lat": -32.9833, "lon": 27.8667},
            {"name": "Mthatha", "postal_codes": ["5099-5100"], "lat": -31.5833, "lon": 28.7833},
            {"name": "King William's Town", "postal_codes": ["5600-5605"], "lat": -32.8833, "lon": 27.4000},
        ]
    },
    "FS": {
        "name": "Free State",
        "name_af": "Vrystaat",
        "name_zu": "iFreyistata",
        "capital": "Bloemfontein",
        "cities": [
            {"name": "Bloemfontein", "postal_codes": ["9300-9399"], "lat": -29.0852, "lon": 26.1596},
            {"name": "Welkom", "postal_codes": ["9459-9470"], "lat": -27.9833, "lon": 26.7333},
            {"name": "Sasolburg", "postal_codes": ["1947-1949"], "lat": -26.8167, "lon": 27.8167},
            {"name": "Bethlehem", "postal_codes": ["9700-9701"], "lat": -28.2333, "lon": 28.3000},
        ]
    },
    "LP": {
        "name": "Limpopo",
        "name_af": "Limpopo",
        "name_zu": "iLimpopo",
        "capital": "Polokwane",
        "cities": [
            {"name": "Polokwane", "postal_codes": ["0699-0799"], "lat": -23.8943, "lon": 29.4485},
            {"name": "Thabazimbi", "postal_codes": ["0380-0381"], "lat": -24.6000, "lon": 27.4167},
            {"name": "Musina", "postal_codes": ["0900-0901"], "lat": -22.1500, "lon": 30.0333},
            {"name": "Phalaborwa", "postal_codes": ["1389-1390"], "lat": -23.9417, "lon": 31.1417},
        ]
    },
    "MP": {
        "name": "Mpumalanga",
        "name_af": "Mpumalanga",
        "name_zu": "iMpumalanga",
        "capital": "Mbombela",
        "cities": [
            {"name": "Mbombela", "postal_codes": ["1200-1240"], "lat": -25.4650, "lon": 30.9853},
            {"name": "Nelspruit", "postal_codes": ["1200-1214"], "lat": -25.4741, "lon": 30.9669},
            {"name": "Witbank", "postal_codes": ["1034-1040"], "lat": -25.8711, "lon": 29.1792},
            {"name": "Secunda", "postal_codes": ["2300-2302"], "lat": -26.5500, "lon": 29.1667},
            {"name": "Middleburg", "postal_codes": ["1050-1060"], "lat": -25.7751, "lon": 29.4648},
        ]
    },
    "NW": {
        "name": "North West",
        "name_af": "Noord-Wes",
        "name_zu": "iNyakatho-Ntshonalanga",
        "capital": "Mahikeng",
        "cities": [
            {"name": "Mahikeng", "postal_codes": ["2740-2799"], "lat": -25.8500, "lon": 25.6333},
            {"name": "Rustenburg", "postal_codes": ["0299-0300"], "lat": -25.6656, "lon": 27.2564},
            {"name": "Klerksdorp", "postal_codes": ["2570-2571"], "lat": -26.8667, "lon": 26.6667},
            {"name": "Potchefstroom", "postal_codes": ["2520-2531"], "lat": -26.7147, "lon": 27.0958},
        ]
    },
    "NC": {
        "name": "Northern Cape",
        "name_af": "Noord-Kaap",
        "name_zu": "iKapa ya Botjhabela",
        "capital": "Kimberley",
        "cities": [
            {"name": "Kimberley", "postal_codes": ["8300-8399"], "lat": -28.7282, "lon": 24.7499},
            {"name": "Upington", "postal_codes": ["8800-8802"], "lat": -28.4500, "lon": 21.2500},
            {"name": "Springs", "postal_codes": ["1559-1560"], "lat": -26.1556, "lon": 28.4478},
            {"name": "De Aar", "postal_codes": ["7000-7002"], "lat": -30.6500, "lon": 24.0167},
        ]
    }
}

@tool
def get_provinces(lang: str = "en") -> str:
    """
    获取南非省份列表
    
    参数:
        lang: 语言代码 (en/af/zu/xh等)
    """
    result = []
    for code, data in PROVINCES_CITIES.items():
        name_key = f"name_{lang}" if f"name_{lang}" in data else "name"
        result.append({
            "code": code,
            "name": data.get(name_key, data["name"]),
            "capital": data["capital"],
            "city_count": len(data["cities"])
        })
    return json.dumps({"success": True, "provinces": result})

@tool
def get_cities_by_province(province_code: str, lang: str = "en") -> str:
    """
    获取指定省份的城市列表
    
    参数:
        province_code: 省份代码 (GP/WC/KZN等)
        lang: 语言代码
    """
    province_code = province_code.upper()
    if province_code not in PROVINCES_CITIES:
        return json.dumps({"success": False, "error": "Province not found"})
    
    data = PROVINCES_CITIES[province_code]
    cities = []
    for city in data["cities"]:
        cities.append({
            "name": city["name"],
            "postal_codes": city["postal_codes"],
            "lat": city["lat"],
            "lon": city["lon"]
        })
    
    name_key = f"name_{lang}" if f"name_{lang}" in data else "name"
    return json.dumps({
        "success": True,
        "province": {"code": province_code, "name": data.get(name_key, data["name"])},
        "cities": cities
    })

# ==================== 手机号/邮编验证规则 ====================

@tool
def validate_sa_phone(phone: str) -> str:
    """
    验证南非手机号格式
    
    南非手机号格式:
    - +27 + 运营商号段 + 用户号码 (国际格式)
    - 0 + 运营商号段 + 用户号码 (国内格式)
    
    运营商号段: 60, 61, 62, 71, 72, 73, 74, 76, 78, 79, 81, 82, 83, 84
    """
    # 移除空格和破折号
    clean = re.sub(r'[\s\-\(\)]', '', phone)
    
    # 国际格式: +27xxxxxxxxx
    if clean.startswith('+27') and len(clean) == 12:
        prefix = clean[3:5]
        if prefix in ['60', '61', '62', '71', '72', '73', '74', '76', '78', '79', '81', '82', '83', '84']:
            return json.dumps({
                "valid": True,
                "original": phone,
                "normalized": clean,
                "format": "international",
                "country_code": "+27",
                "number": clean[3:]
            })
    
    # 国内格式: 0xxxxxxxxx
    if clean.startswith('0') and len(clean) == 10:
        prefix = clean[1:3]
        if prefix in ['60', '61', '62', '71', '72', '73', '74', '76', '78', '79', '81', '82', '83', '84']:
            return json.dumps({
                "valid": True,
                "original": phone,
                "normalized": f"+27{clean[1:]}",
                "format": "local",
                "country_code": "+27",
                "number": clean[1:]
            })
    
    return json.dumps({
        "valid": False,
        "original": phone,
        "error": "Invalid South African phone number format",
        "hint": "Use format: +27 XX XXX XXXX or 0XX XXX XXXX"
    })

@tool
def validate_sa_postal_code(postal_code: str) -> str:
    """
    验证南非邮编格式
    
    南非邮编: 4位数字
    """
    clean = re.sub(r'[\s]', '', postal_code)
    
    if re.match(r'^\d{4}$', clean):
        return json.dumps({
            "valid": True,
            "original": postal_code,
            "normalized": clean,
            "format": "standard"
        })
    
    return json.dumps({
        "valid": False,
        "original": postal_code,
        "error": "Invalid South African postal code",
        "hint": "Must be exactly 4 digits (e.g., 2000)"
    })

@tool
def validate_sa_address(province: str, city: str, postal_code: str, street: str) -> str:
    """
    验证南非完整地址
    """
    # 验证省份
    if province.upper() not in PROVINCES_CITIES:
        return json.dumps({
            "valid": False,
            "field": "province",
            "error": "Invalid province code"
        })
    
    # 验证邮编
    postal_result = json.loads(validate_sa_postal_code(postal_code))
    if not postal_result.get("valid"):
        return json.dumps({
            "valid": False,
            "field": "postal_code",
            "error": postal_result.get("error")
        })
    
    # 验证城市（检查是否属于该省份）
    province_data = PROVINCES_CITIES[province.upper()]
    city_names = [c["name"].lower() for c in province_data["cities"]]
    
    if city.lower() not in city_names:
        # 可能是小城市，检查邮编
        postal_found = False
        for c in province_data["cities"]:
            if postal_code in c["postal_codes"]:
                postal_found = True
                break
        
        if not postal_found:
            return json.dumps({
                "valid": False,
                "field": "city",
                "error": "City does not match postal code in this province"
            })
    
    return json.dumps({
        "valid": True,
        "province": province.upper(),
        "city": city,
        "postal_code": postal_result["normalized"],
        "street": street
    })

# ==================== 弱网环境适配 ====================

# 网络状态模拟
NETWORK_CONDITIONS = {
    "online": {"latency": 100, "packet_loss": 0, "bandwidth_mbps": 50},
    "slow_3g": {"latency": 400, "packet_loss": 5, "bandwidth_mbps": 0.4},
    "fast_3g": {"latency": 200, "packet_loss": 2, "bandwidth_mbps": 2},
    "4g": {"latency": 100, "packet_loss": 0, "bandwidth_mbps": 20},
    "offline": {"latency": 0, "packet_loss": 100, "bandwidth_mbps": 0},
}

@tool
def check_network_status() -> str:
    """
    检查当前网络状态
    （实际应用中会调用真实网络检测API）
    """
    return json.dumps({
        "success": True,
        "status": "online",
        "latency_ms": NETWORK_CONDITIONS["online"]["latency"],
        "bandwidth_mbps": NETWORK_CONDITIONS["online"]["bandwidth_mbps"],
        "recommendation": "full_feature_mode"
    })

@tool
def get_offline_cache_policy() -> str:
    """
    获取离线缓存策略
    """
    return json.dumps({
        "success": True,
        "cache_rules": [
            {"type": "product_catalog", "ttl_hours": 24, "max_size_mb": 50},
            {"type": "user_profile", "ttl_hours": 1, "max_size_mb": 1},
            {"type": "cart_items", "ttl_hours": 168, "max_size_mb": 5},
            {"type": "recent_orders", "ttl_hours": 24, "max_size_mb": 2},
        ],
        "offline_capabilities": [
            "browse_cached_products",
            "manage_cart",
            "view_order_history",
            "queue_orders_for_sync"
        ],
        "sync_priority": ["orders", "payments", "cart", "profile"]
    })

@tool
def estimate_delivery_time(province: str, city: str) -> str:
    """
    估算配送时间
    
    参数:
        province: 省份代码
        city: 城市名
    """
    province_code = province.upper()
    
    # 配送时间基准（工作日）
    base_delivery = {
        "GP": 1,  # Gauteng - 1天
        "WC": 2,  # Western Cape - 2天
        "KZN": 2, # KwaZulu-Natal - 2天
        "EC": 3,  # Eastern Cape - 3天
        "FS": 2,  # Free State - 2天
        "LP": 3,  # Limpopo - 3天
        "MP": 2,  # Mpumalanga - 2天
        "NW": 3,  # North West - 3天
        "NC": 4,  # Northern Cape - 4天
    }
    
    days = base_delivery.get(province_code, 3)
    
    return json.dumps({
        "success": True,
        "province": province_code,
        "city": city,
        "estimated_days": days,
        "note": f"Delivery within {days} business days for {city}"
    })

@tool
def calculate_shipping_fee(province: str, cart_total_cents: int) -> str:
    """
    计算配送费用
    
    参数:
        province: 省份代码
        cart_total_cents: 购物车总金额（分）
    """
    province_code = province.upper()
    
    # 免费配送门槛和费率
    FREE_SHIPPING_THRESHOLD = 50000  # R500
    STANDARD_FEE = 5990              # R59.90
    REMOTE_FEE = 9900                # R99.00 (偏远地区)
    
    remote_provinces = ["NC", "LP", "NW"]  # 偏远省份
    
    if cart_total_cents >= FREE_SHIPPING_THRESHOLD:
        fee = 0
    elif province_code in remote_provinces:
        fee = REMOTE_FEE
    else:
        fee = STANDARD_FEE
    
    final_total = cart_total_cents + fee
    
    return json.dumps({
        "success": True,
        "province": province_code,
        "cart_total": f"R{cart_total_cents/100:.2f}",
        "cart_total_cents": cart_total_cents,
        "shipping_fee": f"R{fee/100:.2f}",
        "shipping_fee_cents": fee,
        "free_shipping_threshold": f"R{FREE_SHIPPING_THRESHOLD/100:.2f}",
        "qualifies_free_shipping": cart_total_cents >= FREE_SHIPPING_THRESHOLD,
        "final_total": f"R{final_total/100:.2f}",
        "final_total_cents": final_total
    })

# ==================== 格式化辅助函数 ====================

@tool
def format_phone_international(phone: str) -> str:
    """将手机号转换为国际格式"""
    result = json.loads(validate_sa_phone(phone))
    if result.get("valid"):
        return f"+27 {result['number'][0:2]} {result['number'][2:5]} {result['number'][5:]}"
    return phone

@tool
def format_address_display(province: str, city: str, street: str, postal_code: str) -> str:
    """格式化地址显示"""
    province_name = PROVINCES_CITIES.get(province.upper(), {}).get("name", province)
    return f"{street}, {city}, {province_name} {postal_code}, South Africa"
