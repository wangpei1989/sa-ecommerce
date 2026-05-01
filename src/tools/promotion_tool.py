"""
营销工具
优惠券、促销活动、积分系统
"""
import json
import uuid
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from langchain.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context

# 优惠券数据
coupons_db: Dict[str, Dict[str, Any]] = {}

# 促销活动
promotions_db: Dict[str, Dict[str, Any]] = {}

# 用户优惠券领取记录
user_coupons: Dict[str, list] = {}

# 初始化示例数据
def init_promotions():
    global promotions_db, coupons_db
    
    # 首单优惠
    promotions_db["FIRST_ORDER"] = {
        "id": "FIRST_ORDER",
        "name": "首单立减",
        "description": "新用户首单立减 R50",
        "discount_type": "fixed",
        "discount_value": 5000,  # 分
        "min_order_amount": 10000,  # 最低消费100 ZAR
        "end_date": "2025-12-31",
        "is_active": True,
    }
    
    # 满减活动
    promotions_db["FREESHIP500"] = {
        "id": "FREESHIP500",
        "name": "满500免运费",
        "description": "订单满R500免运费",
        "discount_type": "free_shipping",
        "min_order_amount": 50000,
        "end_date": "2025-12-31",
        "is_active": True,
    }
    
    # 示例优惠券
    coupons_db["WELCOME10"] = {
        "code": "WELCOME10",
        "name": "新人10%券",
        "discount_type": "percent",
        "discount_value": 10,  # 10%
        "max_discount": 10000,  # 最高减100 ZAR
        "min_order_amount": 5000,  # 最低消费50 ZAR
        "valid_from": "2025-01-01",
        "valid_until": "2025-12-31",
        "total_count": 1000,
        "remaining": 500,
        "is_active": True,
    }


init_promotions()


@tool
def get_active_promotions() -> str:
    """
    获取当前有效促销活动
    
    Returns:
        促销活动列表JSON
    """
    active = [p for p in promotions_db.values() if p.get("is_active", True)]
    
    return json.dumps({
        "success": True,
        "count": len(active),
        "promotions": active
    })


@tool
def claim_coupon(user_id: str, coupon_code: str) -> str:
    """
    领取优惠券
    
    Args:
        user_id: 用户ID
        coupon_code: 优惠券码
        
    Returns:
        领取结果JSON
    """
    ctx = request_context.get() or new_context(method="claim_coupon")
    
    coupon = coupons_db.get(coupon_code)
    if not coupon:
        return json.dumps({
            "success": False,
            "error": "Coupon not found"
        })
    
    if not coupon.get("is_active", True):
        return json.dumps({
            "success": False,
            "error": "Coupon is inactive"
        })
    
    if coupon["remaining"] <= 0:
        return json.dumps({
            "success": False,
            "error": "Coupon exhausted"
        })
    
    # 检查用户是否已领取
    if user_id not in user_coupons:
        user_coupons[user_id] = []
    
    if coupon_code in user_coupons[user_id]:
        return json.dumps({
            "success": False,
            "error": "You have already claimed this coupon"
        })
    
    # 领取
    coupon["remaining"] -= 1
    user_coupons[user_id].append(coupon_code)
    
    return json.dumps({
        "success": True,
        "coupon": {
            "code": coupon["code"],
            "name": coupon["name"],
            "discount_type": coupon["discount_type"],
            "discount_value": coupon["discount_value"],
            "valid_until": coupon["valid_until"],
        }
    })


@tool
def get_user_coupons(user_id: str, status: str = "available") -> str:
    """
    获取用户优惠券
    
    Args:
        user_id: 用户ID
        status: 状态 (available/used/expired)
        
    Returns:
        优惠券列表JSON
    """
    user_codes = user_coupons.get(user_id, [])
    
    result = []
    for code in user_codes:
        coupon = coupons_db.get(code)
        if coupon:
            result.append(coupon)
    
    return json.dumps({
        "success": True,
        "count": len(result),
        "coupons": result
    })


@tool
def validate_coupon(order_amount: int, coupon_code: str) -> str:
    """
    验证优惠券并计算优惠
    
    Args:
        order_amount: 订单金额(单位: 分)
        coupon_code: 优惠券码
        
    Returns:
        优惠结果JSON
    """
    ctx = request_context.get() or new_context(method="validate_coupon")
    
    coupon = coupons_db.get(coupon_code)
    if not coupon:
        return json.dumps({
            "success": False,
            "error": "Coupon not found"
        })
    
    # 检查有效期
    now = datetime.now()
    valid_until = datetime.strptime(coupon["valid_until"], "%Y-%m-%d")
    if now > valid_until:
        return json.dumps({
            "success": False,
            "error": "Coupon expired"
        })
    
    # 检查最低消费
    if order_amount < coupon["min_order_amount"]:
        return json.dumps({
            "success": False,
            "error": f"Minimum order amount: R{coupon['min_order_amount']/100}"
        })
    
    # 计算优惠
    discount = 0
    if coupon["discount_type"] == "fixed":
        discount = coupon["discount_value"]
    elif coupon["discount_type"] == "percent":
        discount = int(order_amount * coupon["discount_value"] / 100)
        discount = min(discount, coupon["max_discount"])
    
    return json.dumps({
        "success": True,
        "coupon_code": coupon_code,
        "original_amount": order_amount,
        "discount": discount,
        "final_amount": order_amount - discount,
        "currency": "ZAR"
    })


@tool
def calculate_loyalty_points(order_amount: int) -> str:
    """
    计算订单可获得积分
    
    Args:
        order_amount: 订单金额(单位: 分)
        
    Returns:
        积分信息JSON
    """
    # 每100 ZAR得1积分
    points = order_amount // 10000
    
    return json.dumps({
        "success": True,
        "order_amount": order_amount,
        "earned_points": points,
        "currency": "ZAR"
    })
