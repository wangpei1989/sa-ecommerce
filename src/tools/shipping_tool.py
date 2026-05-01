"""
物流追踪工具
提供订单配送追踪、物流信息查询功能
"""
import json
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from langchain.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context

# 物流状态
SHIPPING_STATUS = {
    "PICKUP": "提货中",
    "IN_TRANSIT": "运输中",
    "OUT_FOR_DELIVERY": "派送中",
    "DELIVERED": "已送达",
    "FAILED": "配送失败",
    "RETURNED": "退回中",
}

# 南非本地物流公司
LOGISTICS_PROVIDERS = {
    "SAPO": "南非邮政",
    "DPE": "DPE快递",
    "RAM": "RAM快递",
    "SPEEDY": "Speedy快递",
}


@tool
def track_shipment(tracking_number: str) -> str:
    """
    追踪物流信息
    
    Args:
        tracking_number: 物流单号
        
    Returns:
        物流信息JSON
    """
    ctx = request_context.get() or new_context(method="track_shipment")
    
    # 模拟物流轨迹数据
    # 实际项目中应调用物流API
    now = datetime.utcnow()
    
    tracking_info = {
        "tracking_number": tracking_number,
        "provider": "DPE",
        "status": SHIPPING_STATUS["IN_TRANSIT"],
        "estimated_delivery": (now + timedelta(days=3)).strftime("%Y-%m-%d"),
        "current_location": "约翰内斯堡分拨中心",
        "events": [
            {
                "time": now.isoformat(),
                "status": "包裹已到达约翰内斯堡分拨中心",
                "location": "约翰内斯堡"
            },
            {
                "time": (now - timedelta(hours=12)).isoformat(),
                "status": "包裹已从开普敦发出",
                "location": "开普敦"
            },
            {
                "time": (now - timedelta(days=1)).isoformat(),
                "status": "商家已发货",
                "location": "仓库"
            },
        ]
    }
    
    return json.dumps({
        "success": True,
        "tracking": tracking_info
    }, ensure_ascii=False)


@tool
def get_pickup_points(province: Optional[str] = None, city: Optional[str] = None) -> str:
    """
    获取自提点列表
    
    Args:
        province: 省份(可选)
        city: 城市(可选)
        
    Returns:
        自提点列表JSON
    """
    # 模拟自提点数据
    pickup_points = [
        {
            "id": "PP001",
            "name": "约堡市中心自提点",
            "address": "Johannesburg CBD, 123 Main Street",
            "province": "Gauteng",
            "city": "Johannesburg",
            "hours": "08:00-20:00",
            "phone": "+27 11 123 4567"
        },
        {
            "id": "PP002",
            "name": "开普敦海滨自提点",
            "address": "Cape Town Waterfront, Shop 45",
            "province": "Western Cape",
            "city": "Cape Town",
            "hours": "09:00-21:00",
            "phone": "+27 21 987 6543"
        },
        {
            "id": "PP003",
            "name": "德班商业区自提点",
            "address": "Durban CBD, 456 Victoria Street",
            "province": "KwaZulu-Natal",
            "city": "Durban",
            "hours": "08:30-19:00",
            "phone": "+27 31 555 1234"
        },
    ]
    
    # 过滤
    if province:
        pickup_points = [p for p in pickup_points if p["province"] == province]
    if city:
        pickup_points = [p for p in pickup_points if p["city"] == city]
    
    return json.dumps({
        "success": True,
        "count": len(pickup_points),
        "pickup_points": pickup_points
    }, ensure_ascii=False)


@tool
def calculate_shipping_fee(
    weight: float,
    province: str,
    is_express: bool = False
) -> str:
    """
    计算运费
    
    Args:
        weight: 商品重量(kg)
        province: 送达省份
        is_express: 是否为加急配送
        
    Returns:
        运费信息JSON (单位: 分)
    """
    ctx = request_context.get() or new_context(method="calculate_shipping_fee")
    
    # 基础运费规则 (单位: 分)
    base_fee = 3000  # 30 ZAR
    
    # 按重量加费
    weight_fee = int(weight * 1000) * 10  # 每0.1kg加10分
    
    # 偏远地区附加费
    remote_provinces = ["Northern Cape", "Limpopo", "Mpumalanga"]
    remote_fee = 2000 if province in remote_provinces else 0
    
    # 加急费用
    express_fee = 5000 if is_express else 0
    
    total_fee = base_fee + weight_fee + remote_fee + express_fee
    
    return json.dumps({
        "success": True,
        "fee_breakdown": {
            "base_fee": base_fee,
            "weight_fee": weight_fee,
            "remote_fee": remote_fee,
            "express_fee": express_fee
        },
        "total_fee": total_fee,
        "currency": "ZAR",
        "currency_display": f"R{total_fee/100:.2f}"
    })
