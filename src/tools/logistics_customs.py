"""
南非跨境物流与清关模块
包含：物流追踪、自提点查询、运费计算（含偏远地区附加费）、清关流程说明
"""
import json
import re
from datetime import datetime, timedelta
from typing import Optional, List
from langchain.tools import tool

# ==================== 物流追踪模块 ====================

# 物流状态定义
LOGISTICS_STATUS = {
    "pending": {"en": "Pending", "zh": "待处理", "order": 0},
    "picked_up": {"en": "Picked Up", "zh": "已取件", "order": 1},
    "in_transit": {"en": "In Transit", "zh": "运输中", "order": 2},
    "at_customs": {"en": "At Customs", "zh": "清关中", "order": 3},
    "customs_cleared": {"en": "Customs Cleared", "zh": "清关完成", "order": 4},
    "out_for_delivery": {"en": "Out for Delivery", "zh": "派送中", "order": 5},
    "delivered": {"en": "Delivered", "zh": "已签收", "order": 6},
    "returned": {"en": "Returned", "zh": "退回", "order": 7},
    "exception": {"en": "Exception", "zh": "异常", "order": 8},
}

# 物流节点定义
TRACKING_NODES = {
    "JHB_HUB": {"name": "Johannesburg Hub", "city": "Johannesburg", "province": "GP", "lat": -26.2041, "lon": 28.0473},
    "CPT_HUB": {"name": "Cape Town Hub", "city": "Cape Town", "province": "WC", "lat": -33.9249, "lon": 18.4241},
    "DUR_HUB": {"name": "Durban Port", "city": "Durban", "province": "KZN", "lat": -29.8587, "lon": 31.0218},
    "PE_PORT": {"name": "Port Elizabeth Port", "city": "Port Elizabeth", "province": "EC", "lat": -33.9608, "lon": 25.6142},
    "NLS_HUB": {"name": "Nelspruit Distribution", "city": "Mbombela", "province": "MP", "lat": -25.4650, "lon": 30.9853},
    "KIM_HUB": {"name": "Kimberley Hub", "city": "Kimberley", "province": "NC", "lat": -28.7282, "lon": 24.7499},
}

# 物流轨迹数据存储（模拟）
TRACKING_DATA = {}

def _generate_tracking_events(tracking_number: str) -> List[dict]:
    """生成模拟物流轨迹"""
    base_time = datetime.now() - timedelta(days=2)
    events = [
        {"time": (base_time - timedelta(hours=12)).isoformat(), "status": "picked_up", "location": "Customer Address", "description": "Package picked up from sender"},
        {"time": (base_time - timedelta(hours=8)).isoformat(), "status": "in_transit", "location": "JHB_HUB", "description": "Arrived at Johannesburg sorting center"},
        {"time": (base_time - timedelta(hours=4)).isoformat(), "status": "in_transit", "location": "JHB_HUB", "description": "Departed from Johannesburg sorting center"},
        {"time": (base_time - timedelta(hours=2)).isoformat(), "status": "at_customs", "location": "DUR_HUB", "description": "Arrived at customs for inspection"},
        {"time": (base_time).isoformat(), "status": "customs_cleared", "location": "DUR_HUB", "description": "Customs cleared, ready for domestic delivery"},
        {"time": (datetime.now() - timedelta(hours=1)).isoformat(), "status": "out_for_delivery", "location": "Local Delivery Station", "description": "Out for delivery to recipient"},
    ]
    return events

@tool
def track_shipment(tracking_number: str) -> str:
    """
    追踪物流轨迹
    
    参数:
        tracking_number: 物流单号
    
    返回:
        物流轨迹详情
    """
    # 验证单号格式
    if not re.match(r'^[A-Z]{2}\d{10,14}$', tracking_number.upper()):
        # 尝试生成模拟数据
        tracking_number = f"SA{hash(tracking_number) % 10000000000:010d}"
    
    # 获取或生成轨迹数据
    if tracking_number not in TRACKING_DATA:
        TRACKING_DATA[tracking_number] = {
            "tracking_number": tracking_number,
            "carrier": "South Africa Post",
            "service_type": "Express Delivery",
            "estimated_delivery": (datetime.now() + timedelta(days=1)).isoformat(),
            "current_status": "out_for_delivery",
            "events": _generate_tracking_events(tracking_number)
        }
    
    data = TRACKING_DATA[tracking_number]
    
    return json.dumps({
        "success": True,
        "tracking_number": data["tracking_number"],
        "carrier": data["carrier"],
        "service_type": data["service_type"],
        "current_status": {
            "code": data["current_status"],
            "en": LOGISTICS_STATUS[data["current_status"]]["en"],
            "zh": LOGISTICS_STATUS[data["current_status"]]["zh"]
        },
        "estimated_delivery": data["estimated_delivery"],
        "events": [
            {
                "time": e["time"],
                "status": e["status"],
                "status_text": LOGISTICS_STATUS[e["status"]]["en"],
                "location": e["location"],
                "description": e["description"]
            }
            for e in data["events"]
        ]
    }, ensure_ascii=False)

@tool
def verify_tracking_number(tracking_number: str) -> str:
    """
    验证物流单号格式
    
    支持格式:
    - SA + 10-14位数字
    - 国际E格式
    - 国内标准格式
    """
    clean = tracking_number.strip().upper()
    
    patterns = [
        (r'^SA\d{10,14}$', 'domestic_express'),
        (r'^[A-Z]{2}\d{9}[A-Z]{2}$', 'international_ems'),
        (r'^\d{13}$', 'sa_post_standard'),
    ]
    
    matched = None
    for pattern, fmt in patterns:
        if re.match(pattern, clean):
            matched = fmt
            break
    
    if matched:
        return json.dumps({
            "valid": True,
            "tracking_number": clean,
            "format_type": matched
        })
    
    return json.dumps({
        "valid": False,
        "tracking_number": clean,
        "error": "Invalid tracking number format",
        "supported_formats": [
            "SA + 10-14 digits",
            "XX + 9 digits + XX (International EMS)",
            "13 digits (SA Post Standard)"
        ]
    })

# ==================== 自提点查询模块 ====================

# 合作自提点数据
PICKUP_POINTS = [
    # Gauteng
    {"id": "PP001", "name": "Sandton City Collection Point", "type": "mall", "province": "GP", "city": "Sandton", "address": "Sandton City Shopping Centre, 5th Street, Sandton", "postal_code": "2196", "lat": -26.0535, "lon": 28.0569, "hours": "08:00-20:00", "parking": True, "services": ["24h", "parking", "wheelchair"]},
    {"id": "PP002", "name": "Rosebank Post Office", "type": "post_office", "province": "GP", "city": "Rosebank", "address": "15 The Zone, Oxford Road, Rosebank", "postal_code": "2196", "lat": -26.1457, "lon": 28.0417, "hours": "09:00-17:00", "parking": False, "services": ["wheelchair"]},
    {"id": "PP003", "name": "Fourways Mall Pickup", "type": "mall", "province": "GP", "city": "Fourways", "address": "Fourways Mall, William Nicol Drive", "postal_code": "2055", "lat": -26.0172, "lon": 28.0085, "hours": "09:00-19:00", "parking": True, "services": ["parking", "wheelchair", "kids_area"]},
    {"id": "PP004", "name": "Menlyn Park Parcel Locker", "type": "locker", "province": "GP", "city": "Menlyn", "address": "Menlyn Park Shopping Centre, Lois Avenue", "postal_code": "0181", "lat": -25.7833, "lon": 28.2750, "hours": "24h", "parking": True, "services": ["24h", "parking", "locker"]},
    {"id": "PP005", "name": "Centurion Post Office", "type": "post_office", "province": "GP", "city": "Centurion", "address": "Centurion Mall, Old Johannesburg Road", "postal_code": "0157", "lat": -25.8589, "lon": 28.1858, "hours": "08:30-17:00", "parking": True, "services": ["parking", "wheelchair"]},
    
    # Western Cape
    {"id": "PP101", "name": "V&A Waterfront Collection", "type": "mall", "province": "WC", "city": "Cape Town", "address": "V&A Waterfront, Dock Road", "postal_code": "8001", "lat": -33.9047, "lon": 18.4183, "hours": "10:00-21:00", "parking": True, "services": ["parking", "wheelchair", "kids_area", "24h_security"]},
    {"id": "PP102", "name": "Canal Walk Locker", "type": "locker", "province": "WC", "city": "Cape Town", "address": "Canal Walk Shopping Centre, Century Boulevard", "postal_code": "7441", "lat": -33.8294, "lon": 18.5134, "hours": "24h", "parking": True, "services": ["24h", "parking", "locker"]},
    {"id": "PP103", "name": "Stellenbosch University Post", "type": "university", "province": "WC", "city": "Stellenbosch", "address": "Stellenbosch University, Main Campus", "postal_code": "7600", "lat": -33.9321, "lon": 18.8602, "hours": "08:00-18:00", "parking": False, "services": ["wheelchair", "student_discount"]},
    
    # KwaZulu-Natal
    {"id": "PP201", "name": "Gateway Theatre Locker", "type": "locker", "province": "KZN", "city": "Umhlanga", "address": "Gateway Theatre of Shopping, 1 Palm Boulevard", "postal_code": "4319", "lat": -29.7294, "lon": 31.0657, "hours": "24h", "parking": True, "services": ["24h", "parking", "locker"]},
    {"id": "PP202", "name": "Pavilion Shopping Centre", "type": "mall", "province": "KZN", "city": "Durban", "address": "Pavilion Road, Westville", "postal_code": "3629", "lat": -29.8383, "lon": 30.9000, "hours": "09:00-19:00", "parking": True, "services": ["parking", "wheelchair", "kids_area"]},
    {"id": "PP203", "name": "Ballito Checkers Pickup", "type": "supermarket", "province": "KZN", "city": "Ballito", "address": "Checkers Ballito, Ballito Drive", "postal_code": "4424", "lat": -29.5333, "lon": 31.2333, "hours": "08:00-20:00", "parking": True, "services": ["parking"]},
    
    # Eastern Cape
    {"id": "PP301", "name": "Greenacres Shopping Centre", "type": "mall", "province": "EC", "city": "Port Elizabeth", "address": "Greenacres Shopping Centre, Ring Road", "postal_code": "6057", "lat": -33.9608, "lon": 25.6142, "hours": "09:00-18:00", "parking": True, "services": ["parking", "wheelchair"]},
    {"id": "PP302", "name": "Hemingways Mall", "type": "mall", "province": "EC", "city": "East London", "address": "Hemingways Mall, Western Avenue, Cambridge", "postal_code": "5247", "lat": -32.9833, "lon": 27.8667, "hours": "09:00-18:00", "parking": True, "services": ["parking", "wheelchair"]},
    
    # Other provinces
    {"id": "PP401", "name": "Mimosa Mall", "type": "mall", "province": "FS", "city": "Bloemfontein", "address": "Mimosa Mall, Zastron Street", "postal_code": "9301", "lat": -29.0852, "lon": 26.1596, "hours": "09:00-18:00", "parking": True, "services": ["parking"]},
    {"id": "PP501", "name": "Mall of the North", "type": "mall", "province": "LP", "city": "Polokwane", "address": "Mall of the North, c/o Munnik & N1", "postal_code": "0699", "lat": -23.8943, "lon": 29.4485, "hours": "09:00-19:00", "parking": True, "services": ["parking", "wheelchair"]},
    {"id": "PP601", "name": "Riverside Mall", "type": "mall", "province": "MP", "city": "Mbombela", "address": "Riverside Mall, Madiba Drive", "postal_code": "1200", "lat": -25.4650, "lon": 30.9853, "hours": "09:00-18:00", "parking": True, "services": ["parking"]},
    {"id": "PP701", "name": "Rustenburg Mall", "type": "mall", "province": "NW", "city": "Rustenburg", "address": "Rustenburg Mall, 44 Boom Street", "postal_code": "0299", "lat": -25.6656, "lon": 27.2564, "hours": "09:00-18:00", "parking": True, "services": ["parking", "wheelchair"]},
    {"id": "PP801", "name": "Kimberley Mall", "type": "mall", "province": "NC", "city": "Kimberley", "address": "Kimberley Mall, Bultfontein Road", "postal_code": "8301", "lat": -28.7282, "lon": 24.7499, "hours": "09:00-17:30", "parking": True, "services": ["parking"]},
]

@tool
def find_pickup_points(province: str = "", city: str = "", service_type: str = "") -> str:
    """
    查询附近自提点
    
    参数:
        province: 省份代码 (GP/WC/KZN等)
        city: 城市名
        service_type: 服务类型 (mall/post_office/locker/supermarket)
    """
    results = PICKUP_POINTS
    
    if province:
        results = [p for p in results if p["province"].upper() == province.upper()]
    if city:
        results = [p for p in results if city.lower() in p["city"].lower()]
    if service_type:
        results = [p for p in results if p["type"] == service_type]
    
    return json.dumps({
        "success": True,
        "count": len(results),
        "pickup_points": [
            {
                "id": p["id"],
                "name": p["name"],
                "type": p["type"],
                "province": p["province"],
                "city": p["city"],
                "address": p["address"],
                "postal_code": p["postal_code"],
                "hours": p["hours"],
                "parking": p["parking"],
                "services": p["services"]
            }
            for p in results[:20]  # 限制返回数量
        ]
    })

@tool
def get_pickup_point_detail(pickup_id: str) -> str:
    """获取自提点详情"""
    for p in PICKUP_POINTS:
        if p["id"] == pickup_id:
            return json.dumps({
                "success": True,
                "pickup_point": {
                    "id": p["id"],
                    "name": p["name"],
                    "type": p["type"],
                    "province": p["province"],
                    "city": p["city"],
                    "address": p["address"],
                    "postal_code": p["postal_code"],
                    "coordinates": {"lat": p["lat"], "lon": p["lon"]},
                    "hours": p["hours"],
                    "parking": p["parking"],
                    "services": p["services"],
                    "contact": "+27 11 123 4567",
                    "note": "Bring your ID and tracking number when collecting"
                }
            })
    
    return json.dumps({"success": False, "error": "Pickup point not found"})

# ==================== 运费计算模块（增强版） ====================

# 偏远地区定义
REMOTE_AREAS = {
    # Northern Cape - 远北地区
    "8300-8399": {"zone": "remote_north", "surcharge": 4500},  # Kimberley area
    "8800-8899": {"zone": "remote_deep", "surcharge": 7500},   # Upington, deep remote
    "8900-8999": {"zone": "remote_deep", "surcharge": 8500},   # Kalahari area
    
    # Limpopo - 北部边境
    "0900-0999": {"zone": "remote_north", "surcharge": 5000},  # Musina
    "0980-0999": {"zone": "remote_deep", "surcharge": 7000},   # Very remote
    
    # North West - 西部地区
    "2800-2899": {"zone": "remote_west", "surcharge": 3500},
    
    # Eastern Cape - 偏远地区
    "5100-5199": {"zone": "remote_east", "surcharge": 4000},  # Mthatha
    "5200-5299": {"zone": "remote_east", "surcharge": 4500},  # East London
    
    # Mpumalanga - 偏远地区
    "1280-1299": {"zone": "remote_bush", "surcharge": 4500},  # Bush areas
    "1380-1399": {"zone": "remote_bush", "surcharge": 5500},  # Kruger area
}

# 重量费率表（克）
WEIGHT_TIERS = [
    {"max_g": 500, "rate_cents": 2990},
    {"max_g": 1000, "rate_cents": 3990},
    {"max_g": 2000, "rate_cents": 5990},
    {"max_g": 5000, "rate_cents": 8990},
    {"max_g": 10000, "rate_cents": 12990},
    {"max_g": 20000, "rate_cents": 18990},
    {"max_g": 30000, "rate_cents": 24990},
]

@tool
def calculate_shipping_cost(
    province: str,
    city: str,
    postal_code: str,
    weight_grams: int = 1000,
    is_cross_border: bool = False,
    declared_value_cents: int = 0
) -> str:
    """
    计算运费（含偏远地区附加费）
    
    参数:
        province: 省份代码
        city: 城市名
        postal_code: 邮编
        weight_grams: 重量（克）
        is_cross_border: 是否跨境
        declared_value_cents: 申报价值（分）
    
    返回:
        详细运费计算
    """
    province = province.upper()
    
    # 基础配送费用（按重量）
    base_rate = 3990  # 默认1kg费率
    for tier in WEIGHT_TIERS:
        if weight_grams <= tier["max_g"]:
            base_rate = tier["rate_cents"]
            break
    else:
        # 超过30kg，按每kg加收
        extra_kg = (weight_grams - 30000) // 1000
        base_rate = 24990 + extra_kg * 5000
    
    # 偏远地区附加费
    surcharge = 0
    surcharge_reason = ""
    for code_range, info in REMOTE_AREAS.items():
        start, end = code_range.split("-")
        if start <= postal_code <= end:
            surcharge = info["surcharge"]
            surcharge_reason = f"Remote area surcharge ({info['zone']})"
            break
    
    # 省份附加费
    province_extra = {
        "GP": 0,      # 大城市，无附加费
        "WC": 1500,   # 西开普
        "KZN": 1500,  # 夸祖鲁
        "EC": 2500,   # 东开普
        "FS": 2000,   # 自由州
        "LP": 3000,   # 林波波
        "MP": 2000,   # 姆普马兰加
        "NW": 2500,   # 西北省
        "NC": 4500,   # 北开普（最远）
    }
    province_surcharge = province_extra.get(province, 0)
    
    # 跨境附加费
    cross_border_fee = 0
    if is_cross_border:
        cross_border_fee = 9900
        if declared_value_cents > 50000:
            cross_border_fee += 5000  # 高价值商品额外费用
    
    # 免费配送门槛
    FREE_SHIPPING_THRESHOLD = 50000
    
    # 计算总费用
    subtotal = base_rate + surcharge + province_surcharge + cross_border_fee
    final_fee = max(0, subtotal - (FREE_SHIPPING_THRESHOLD // 100 * 100 if declared_value_cents >= FREE_SHIPPING_THRESHOLD else 0))
    
    return json.dumps({
        "success": True,
        "origin": {
            "type": "warehouse",
            "location": "Johannesburg, GP"
        },
        "destination": {
            "province": province,
            "city": city,
            "postal_code": postal_code,
            "is_remote": surcharge > 0,
            "is_cross_border": is_cross_border
        },
        "package": {
            "weight_grams": weight_grams,
            "weight_display": f"{weight_grams/1000:.2f}kg",
            "declared_value_cents": declared_value_cents,
            "declared_value_display": f"R{declared_value_cents/100:.2f}"
        },
        "fees": {
            "base_rate_cents": base_rate,
            "base_rate_display": f"R{base_rate/100:.2f}",
            "remote_surcharge_cents": surcharge,
            "remote_surcharge_display": f"R{surcharge/100:.2f}" if surcharge else "Free",
            "province_surcharge_cents": province_surcharge,
            "province_surcharge_display": f"R{province_surcharge/100:.2f}",
            "cross_border_fee_cents": cross_border_fee,
            "cross_border_fee_display": f"R{cross_border_fee/100:.2f}" if cross_border_fee else "N/A"
        },
        "subtotal_cents": subtotal,
        "subtotal_display": f"R{subtotal/100:.2f}",
        "final_fee_cents": final_fee,
        "final_fee_display": f"R{final_fee/100:.2f}",
        "free_shipping_threshold": f"R{FREE_SHIPPING_THRESHOLD/100:.2f}",
        "surcharge_reason": surcharge_reason
    })

# ==================== 清关流程模块 ====================

# 清关流程定义
CUSTOMS_PROCESS = {
    "cross_border": {
        "steps": [
            {
                "step": 1,
                "name": "Document Preparation",
                "name_zh": "单证准备",
                "description": "Prepare commercial invoice, packing list, and customs declaration",
                "duration": "1-2 days",
                "required_docs": ["Commercial Invoice", "Packing List", "Bill of Lading", "Certificate of Origin"]
            },
            {
                "step": 2,
                "name": "Arrival at Port",
                "name_zh": "抵港",
                "description": "Goods arrive at South African port (Durban, Cape Town, or PE)",
                "duration": "Varies",
                "required_docs": []
            },
            {
                "step": 3,
                "name": "Customs Declaration",
                "name_zh": "报关",
                "description": "Submit customs declaration via SARS e-filing system",
                "duration": "1-3 days",
                "required_docs": ["C&E Declaration", "Import Permit (if required)"]
            },
            {
                "step": 4,
                "name": "Duty & VAT Calculation",
                "name_zh": "税费计算",
                "description": "SARS calculates applicable duties and VAT (15% standard rate)",
                "duration": "1-2 days",
                "required_docs": []
            },
            {
                "step": 5,
                "name": "Inspection & Clearance",
                "name_zh": "查验放行",
                "description": "Physical inspection if selected, then clearance",
                "duration": "2-5 days (may be longer if inspection required)",
                "required_docs": []
            },
            {
                "step": 6,
                "name": "Release & Delivery",
                "name_zh": "放行提货",
                "description": "Goods released for domestic transport",
                "duration": "1-2 days",
                "required_docs": ["Delivery Order", "ID Copy"]
            }
        ],
        "total_duration": "7-21 days",
        "fees": {
            "customs_duty": "0-45% depending on HS code",
            "vat": "15%",
            "excise_duty": "varies",
            "port_handling": "R500-R2000",
            "clearance_fee": "R300-R800"
        }
    },
    "domestic": {
        "steps": [
            {
                "step": 1,
                "name": "Package Collection",
                "name_zh": "揽收",
                "description": "Pickup from sender or warehouse",
                "duration": "Same day",
                "required_docs": []
            },
            {
                "step": 2,
                "name": "Sorting Center",
                "name_zh": "分拣",
                "description": "Processing at local sorting facility",
                "duration": "1 day",
                "required_docs": []
            },
            {
                "step": 3,
                "name": "In-Transit",
                "name_zh": "运输",
                "description": "Moving through logistics network",
                "duration": "1-3 days",
                "required_docs": []
            },
            {
                "step": 4,
                "name": "Last Mile Delivery",
                "name_zh": "末端配送",
                "description": "Final delivery to recipient",
                "duration": "1-2 days",
                "required_docs": []
            }
        ],
        "total_duration": "2-5 days"
    }
}

# 关税税率表（简化版）
DUTY_RATES = {
    "electronics": {"rate": 0.15, "description": "General electronics"},
    "clothing": {"rate": 0.45, "description": "Clothing and apparel"},
    "footwear": {"rate": 0.30, "description": "Shoes and footwear"},
    "home_appliances": {"rate": 0.20, "description": "Home appliances"},
    "cosmetics": {"rate": 0.20, "description": "Beauty products"},
    "food": {"rate": 0.30, "description": "Food products"},
    "books": {"rate": 0, "description": "Books (duty exempt)"},
    "toys": {"rate": 0.30, "description": "Toys and games"},
}

@tool
def get_customs_clearance_info(is_cross_border: bool = True) -> str:
    """
    获取清关流程说明
    
    参数:
        is_cross_border: 是否跨境
    """
    process = CUSTOMS_PROCESS["cross_border"] if is_cross_border else CUSTOMS_PROCESS["domestic"]
    
    return json.dumps({
        "success": True,
        "type": "cross_border" if is_cross_border else "domestic",
        "process_steps": process["steps"],
        "total_duration": process["total_duration"],
        "fees": process.get("fees", {})
    })

@tool
def calculate_customs_duty(
    declared_value_cents: int,
    category: str = "electronics"
) -> str:
    """
    计算预估关税
    
    参数:
        declared_value_cents: 申报价值（分）
        category: 商品类别
    """
    value_zar = declared_value_cents / 100
    
    # 获取税率
    cat_info = DUTY_RATES.get(category.lower(), {"rate": 0.15, "description": "General goods"})
    duty_rate = cat_info["rate"]
    
    # 计算关税
    customs_duty = value_zar * duty_rate
    
    # VAT (15% on value + duty)
    vat_base = value_zar + customs_duty
    vat = vat_base * 0.15
    
    # 总税费
    total_tax = customs_duty + vat
    
    return json.dumps({
        "success": True,
        "declared_value": {
            "cents": declared_value_cents,
            "zar": f"R{value_zar:,.2f}"
        },
        "category": {
            "name": category,
            "description": cat_info["description"]
        },
        "duty_rate": f"{duty_rate*100:.0f}%",
        "customs_duty": {
            "cents": int(customs_duty * 100),
            "zar": f"R{customs_duty:,.2f}"
        },
        "vat": {
            "rate": "15%",
            "cents": int(vat * 100),
            "zar": f"R{vat:,.2f}"
        },
        "total_tax": {
            "cents": int(total_tax * 100),
            "zar": f"R{total_tax:,.2f}"
        },
        "note": "Final duties may vary. Consult a customs broker for accurate assessment."
    })

@tool
def get_prohibited_items() -> str:
    """获取南非禁止进口物品清单"""
    prohibited = [
        {"category": "Firearms & Weapons", "items": "Guns, explosives, ammunition, switchblade knives"},
        {"category": "Narcotics", "items": "Illegal drugs, cannabis products (except medical)"},
        {"category": "Counterfeit", "items": "Fake brands, pirated software"},
        {"category": "Hazardous Materials", "items": "Asbestos, certain chemicals, radioactive materials"},
        {"category": "Wildlife", "items": "Protected species, ivory, rhino horn"},
        {"category": "Food Restrictions", "items": "Fresh meat, dairy products, certain plants"},
        {"category": "Adult Content", "items": "Pornographic materials"},
        {"category": "Political Materials", "items": "Certain publications, hate speech materials"},
    ]
    
    restricted = [
        {"category": "Medications", "note": "Prescription drugs require import permit"},
        {"category": "Alcohol/Tobacco", "note": "Limited quantities for personal use"},
        {"category": "Cash", "note": "Declare cash exceeding R25,000"},
        {"category": "Used Electronics", "note": "May require inspection"},
    ]
    
    return json.dumps({
        "success": True,
        "prohibited": prohibited,
        "restricted": restricted,
        "general_tips": [
            "Keep receipts for all items",
            "Declare accurate values",
            "Use original packaging when possible",
            "Check SARS website for latest regulations"
        ]
    })

@tool
def estimate_total_delivery_time(
    is_cross_border: bool,
    province: str,
    shipping_method: str = "standard"
) -> str:
    """
    估算总配送时间
    
    参数:
        is_cross_border: 是否跨境
        province: 省份代码
        shipping_method: 配送方式 (standard/express/economy)
    """
    province = province.upper()
    
    # 基础国内配送时间
    base_days = {
        "GP": 1, "WC": 2, "KZN": 2, "EC": 3, "FS": 2,
        "LP": 3, "MP": 2, "NW": 3, "NC": 4
    }
    domestic_days = base_days.get(province, 3)
    
    # 配送方式系数
    method_multiplier = {
        "economy": 1.5,
        "standard": 1.0,
        "express": 0.6
    }
    
    if is_cross_border:
        # 跨境：清关 + 国内
        customs_days = 7  # 基础清关
        total = int((domestic_days + customs_days) * method_multiplier.get(shipping_method, 1.0))
    else:
        total = int(domestic_days * method_multiplier.get(shipping_method, 1.0))
    
    return json.dumps({
        "success": True,
        "is_cross_border": is_cross_border,
        "destination_province": province,
        "shipping_method": shipping_method,
        "breakdown": {
            "customs_clearance_days": 7 if is_cross_border else 0,
            "domestic_transit_days": domestic_days,
            "method_multiplier": method_multiplier.get(shipping_method, 1.0)
        },
        "estimated_days": max(1, total),
        "estimated_date": (datetime.now() + timedelta(days=max(1, total))).strftime("%Y-%m-%d"),
        "note": "Estimates may vary during peak seasons or holidays"
    })
