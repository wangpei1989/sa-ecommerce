"""
南非跨境电商 - 营销功能模块
包含：促销活动、优惠券、积分系统
"""
import json
import re
from datetime import datetime, timedelta
from typing import Optional, List
from langchain.tools import tool

# ==================== 数据存储（模拟） ====================

# 促销活动
PROMOTIONS = {}

# 优惠券
COUPONS = {}

# 用户积分
USER_POINTS = {}

# 积分记录
POINTS_HISTORY = {}

# ==================== 促销活动模块 ====================

# 促销类型
PROMOTION_TYPES = {
    "flash_sale": "Flash Sale",
    "discount": "Discount",
    "bundle": "Bundle Deal",
    "buy_x_get_y": "Buy X Get Y",
    "free_shipping": "Free Shipping"
}

# 促销状态
PROMOTION_STATUS = {
    "upcoming": "Upcoming",
    "active": "Active",
    "ended": "Ended",
    "cancelled": "Cancelled"
}

def _init_default_promotions():
    """初始化默认促销活动"""
    if not PROMOTIONS:
        now = datetime.now()
        PROMOTIONS["PROMO001"] = {
            "promo_id": "PROMO001",
            "name": "Summer Flash Sale",
            "name_zh": "夏季闪购",
            "type": "flash_sale",
            "description": "Up to 50% off on electronics",
            "discount_value": 50,
            "discount_type": "percentage",
            "max_discount_cents": 50000,
            "min_order_cents": 10000,
            "status": "active",
            "start_time": (now - timedelta(days=1)).isoformat(),
            "end_time": (now + timedelta(days=7)).isoformat(),
            "applicable_categories": ["Electronics"],
            "applicable_products": [],
            "usage_limit": 1000,
            "used_count": 342
        }
        PROMOTIONS["PROMO002"] = {
            "promo_id": "PROMO002",
            "name": "New User Discount",
            "name_zh": "新用户专享",
            "type": "discount",
            "description": "R50 off for new users",
            "discount_value": 5000,
            "discount_type": "fixed",
            "max_discount_cents": 5000,
            "min_order_cents": 20000,
            "status": "active",
            "start_time": now.isoformat(),
            "end_time": (now + timedelta(days=30)).isoformat(),
            "applicable_categories": [],
            "applicable_products": [],
            "usage_limit": 1,
            "used_count": 0,
            "user_limit": 1
        }
        PROMOTIONS["PROMO003"] = {
            "promo_id": "PROMO003",
            "name": "Fashion Week Sale",
            "name_zh": "时尚周特卖",
            "type": "discount",
            "description": "30% off on all fashion items",
            "discount_value": 30,
            "discount_type": "percentage",
            "max_discount_cents": 30000,
            "min_order_cents": 0,
            "status": "active",
            "start_time": (now - timedelta(days=2)).isoformat(),
            "end_time": (now + timedelta(days=5)).isoformat(),
            "applicable_categories": ["Fashion"],
            "applicable_products": [],
            "usage_limit": 0,
            "used_count": 1234
        }

_init_default_promotions()

@tool
def get_active_promotions() -> str:
    """获取当前有效促销活动"""
    now = datetime.now()
    active = []
    
    for promo in PROMOTIONS.values():
        start = datetime.fromisoformat(promo["start_time"])
        end = datetime.fromisoformat(promo["end_time"])
        
        if start <= now <= end and promo["status"] == "active":
            # 检查是否还有剩余名额
            if promo["usage_limit"] == 0 or promo["used_count"] < promo["usage_limit"]:
                active.append({
                    "promo_id": promo["promo_id"],
                    "name": promo["name"],
                    "name_zh": promo.get("name_zh", ""),
                    "type": promo["type"],
                    "description": promo["description"],
                    "discount": f"{promo['discount_value']}{'%' if promo['discount_type'] == 'percentage' else 'R'} OFF",
                    "max_discount": f"R{promo['max_discount_cents']/100:.2f}" if promo["max_discount_cents"] else "No limit",
                    "min_order": f"R{promo['min_order_cents']/100:.2f}" if promo["min_order_cents"] else "No minimum",
                    "end_time": promo["end_time"],
                    "remaining_uses": promo["usage_limit"] - promo["used_count"] if promo["usage_limit"] else "Unlimited"
                })
    
    return json.dumps({
        "success": True,
        "count": len(active),
        "promotions": active
    })

@tool
def get_promotion_detail(promo_id: str) -> str:
    """获取促销活动详情"""
    if promo_id not in PROMOTIONS:
        return json.dumps({"success": False, "error": "Promotion not found"})
    
    promo = PROMOTIONS[promo_id]
    
    return json.dumps({
        "success": True,
        "promotion": {
            "promo_id": promo["promo_id"],
            "name": promo["name"],
            "name_zh": promo.get("name_zh", ""),
            "type": promo["type"],
            "type_display": PROMOTION_TYPES.get(promo["type"], promo["type"]),
            "description": promo["description"],
            "discount_type": promo["discount_type"],
            "discount_value": promo["discount_value"],
            "max_discount_cents": promo["max_discount_cents"],
            "min_order_cents": promo["min_order_cents"],
            "status": promo["status"],
            "start_time": promo["start_time"],
            "end_time": promo["end_time"],
            "applicable_categories": promo["applicable_categories"],
            "applicable_products": promo["applicable_products"],
            "usage_limit": promo["usage_limit"],
            "used_count": promo["used_count"],
            "remaining": promo["usage_limit"] - promo["used_count"] if promo["usage_limit"] else "Unlimited"
        }
    })

@tool
def calculate_promotion_discount(promo_id: str, order_amount_cents: int, category: str = "", product_id: str = "") -> str:
    """计算促销折扣金额"""
    if promo_id not in PROMOTIONS:
        return json.dumps({"success": False, "error": "Promotion not found"})
    
    promo = PROMOTIONS[promo_id]
    now = datetime.now()
    
    # 检查有效期
    start = datetime.fromisoformat(promo["start_time"])
    end = datetime.fromisoformat(promo["end_time"])
    
    if now < start:
        return json.dumps({"success": False, "error": "Promotion not started yet"})
    if now > end:
        return json.dumps({"success": False, "error": "Promotion has ended"})
    
    # 检查状态
    if promo["status"] != "active":
        return json.dumps({"success": False, "error": "Promotion is not active"})
    
    # 检查最低消费
    if order_amount_cents < promo["min_order_cents"]:
        return json.dumps({
            "success": False,
            "error": f"Minimum order R{promo['min_order_cents']/100:.2f} required"
        })
    
    # 检查适用范围
    if promo["applicable_categories"] and category not in promo["applicable_categories"]:
        return json.dumps({
            "success": False,
            "error": "This promotion is not applicable to this category"
        })
    
    if promo["applicable_products"] and product_id not in promo["applicable_products"]:
        return json.dumps({
            "success": False,
            "error": "This promotion is not applicable to this product"
        })
    
    # 计算折扣
    if promo["discount_type"] == "percentage":
        discount = int(order_amount_cents * promo["discount_value"] / 100)
    else:
        discount = promo["discount_value"]
    
    # 限制最大折扣
    if promo["max_discount_cents"] and discount > promo["max_discount_cents"]:
        discount = promo["max_discount_cents"]
    
    # 确保折扣不超过订单金额
    discount = min(discount, order_amount_cents)
    
    final_amount = order_amount_cents - discount
    
    return json.dumps({
        "success": True,
        "original_amount": f"R{order_amount_cents/100:.2f}",
        "discount_amount": f"R{discount/100:.2f}",
        "final_amount": f"R{final_amount/100:.2f}",
        "promo_id": promo_id,
        "promo_name": promo["name"]
    })

@tool
def create_promotion(merchant_id: str, promo_data: str) -> str:
    """商家创建促销活动"""
    try:
        data = json.loads(promo_data)
    except:
        return json.dumps({"success": False, "error": "Invalid promo data format"})
    
    promo_id = f"PROMO{hash(data['name']) % 1000000:06d}"
    now = datetime.now()
    
    promo = {
        "promo_id": promo_id,
        "merchant_id": merchant_id,
        "name": data["name"],
        "name_zh": data.get("name_zh", ""),
        "type": data.get("type", "discount"),
        "description": data.get("description", ""),
        "discount_value": data["discount_value"],
        "discount_type": data.get("discount_type", "percentage"),
        "max_discount_cents": data.get("max_discount_cents", 0),
        "min_order_cents": data.get("min_order_cents", 0),
        "status": "active",
        "start_time": data.get("start_time", now.isoformat()),
        "end_time": data.get("end_time", (now + timedelta(days=7)).isoformat()),
        "applicable_categories": data.get("categories", []),
        "applicable_products": data.get("products", []),
        "usage_limit": data.get("usage_limit", 0),
        "used_count": 0,
        "created_at": now.isoformat()
    }
    
    PROMOTIONS[promo_id] = promo
    
    return json.dumps({
        "success": True,
        "promo_id": promo_id,
        "message": "Promotion created successfully"
    })

# ==================== 优惠券模块 ====================

# 优惠券状态
COUPON_STATUS = {
    "active": "Active",
    "used": "Used",
    "expired": "Expired",
    "cancelled": "Cancelled"
}

def _init_default_coupons():
    """初始化默认优惠券"""
    if not COUPONS:
        now = datetime.now()
        COUPONS["COUP2024A"] = {
            "code": "COUP2024A",
            "name": "Welcome Coupon",
            "description": "R20 off your first order",
            "discount_type": "fixed",
            "discount_value": 2000,
            "min_order_cents": 10000,
            "max_discount_cents": 2000,
            "status": "active",
            "valid_from": now.isoformat(),
            "valid_until": (now + timedelta(days=30)).isoformat(),
            "total_count": 1000,
            "remaining_count": 876,
            "user_limit": 1,
            "applicable_categories": []
        }
        COUPONS["SAVE30"] = {
            "code": "SAVE30",
            "name": "Save R30",
            "description": "R30 off orders over R300",
            "discount_type": "fixed",
            "discount_value": 3000,
            "min_order_cents": 30000,
            "max_discount_cents": 3000,
            "status": "active",
            "valid_from": now.isoformat(),
            "valid_until": (now + timedelta(days=14)).isoformat(),
            "total_count": 500,
            "remaining_count": 234,
            "user_limit": 3,
            "applicable_categories": []
        }
        COUPONS["FREESHIP"] = {
            "code": "FREESHIP",
            "name": "Free Shipping",
            "description": "Free shipping on any order",
            "discount_type": "free_shipping",
            "discount_value": 0,
            "min_order_cents": 0,
            "max_discount_cents": 5990,
            "status": "active",
            "valid_from": now.isoformat(),
            "valid_until": (now + timedelta(days=7)).isoformat(),
            "total_count": 0,
            "remaining_count": 0,
            "user_limit": 5,
            "applicable_categories": []
        }

_init_default_coupons()

@tool
def get_available_coupons() -> str:
    """获取可用优惠券列表"""
    now = datetime.now()
    available = []
    
    for coupon in COUPONS.values():
        if coupon["status"] != "active":
            continue
        
        valid_until = datetime.fromisoformat(coupon["valid_until"])
        if now > valid_until:
            continue
        
        if coupon["remaining_count"] <= 0:
            continue
        
        available.append({
            "code": coupon["code"],
            "name": coupon["name"],
            "description": coupon["description"],
            "discount": f"R{coupon['discount_value']/100:.0f} OFF" if coupon["discount_type"] == "fixed" else "Free Shipping",
            "min_order": f"R{coupon['min_order_cents']/100:.0f}" if coupon["min_order_cents"] else "No minimum",
            "valid_until": coupon["valid_until"],
            "remaining": coupon["remaining_count"]
        })
    
    return json.dumps({
        "success": True,
        "count": len(available),
        "coupons": available
    })

@tool
def validate_coupon(code: str, order_amount_cents: int, user_id: str = "") -> str:
    """
    验证优惠券
    
    参数:
        code: 优惠券码
        order_amount_cents: 订单金额（分）
        user_id: 用户ID（可选）
    """
    code = code.upper().strip()
    
    if code not in COUPONS:
        return json.dumps({
            "success": False,
            "error": "Invalid coupon code",
            "hint": "Please check the coupon code"
        })
    
    coupon = COUPONS[code]
    now = datetime.now()
    
    # 检查状态
    if coupon["status"] != "active":
        return json.dumps({
            "success": False,
            "error": f"Coupon is {coupon['status']}"
        })
    
    # 检查有效期
    valid_from = datetime.fromisoformat(coupon["valid_from"])
    valid_until = datetime.fromisoformat(coupon["valid_until"])
    
    if now < valid_from:
        return json.dumps({
            "success": False,
            "error": "Coupon is not yet valid"
        })
    if now > valid_until:
        return json.dumps({
            "success": False,
            "error": "Coupon has expired"
        })
    
    # 检查剩余数量
    if coupon["remaining_count"] <= 0:
        return json.dumps({
            "success": False,
            "error": "Coupon is fully redeemed"
        })
    
    # 检查用户使用限制
    if user_id and coupon["user_limit"] > 0:
        user_usage_key = f"{user_id}_{code}"
        # 简化：检查全局使用次数
        used_count = COUPONS[code].get("user_usage", {}).get(user_id, 0)
        if used_count >= coupon["user_limit"]:
            return json.dumps({
                "success": False,
                "error": f"You have already used this coupon {coupon['user_limit']} time(s)"
            })
    
    # 检查最低消费
    if order_amount_cents < coupon["min_order_cents"]:
        return json.dumps({
            "success": False,
            "error": f"Minimum order R{coupon['min_order_cents']/100:.2f} required"
        })
    
    # 计算折扣
    if coupon["discount_type"] == "free_shipping":
        discount = min(5990, order_amount_cents)  # 假设运费最多R59.90
        discount_desc = "Free Shipping"
    else:
        discount = coupon["discount_value"]
        if coupon["max_discount_cents"]:
            discount = min(discount, coupon["max_discount_cents"])
        discount = min(discount, order_amount_cents)
        discount_desc = f"R{discount/100:.2f}"
    
    final_amount = order_amount_cents - discount
    
    return json.dumps({
        "success": True,
        "valid": True,
        "coupon_code": code,
        "coupon_name": coupon["name"],
        "discount_type": coupon["discount_type"],
        "discount_amount": discount_desc,
        "discount_cents": discount,
        "original_amount": f"R{order_amount_cents/100:.2f}",
        "final_amount": f"R{final_amount/100:.2f}",
        "savings": discount_desc
    })

@tool
def redeem_coupon(code: str, user_id: str, order_id: str) -> str:
    """使用优惠券（标记为已使用）"""
    code = code.upper().strip()
    
    if code not in COUPONS:
        return json.dumps({"success": False, "error": "Invalid coupon code"})
    
    coupon = COUPONS[code]
    
    # 更新使用记录
    if "user_usage" not in coupon:
        coupon["user_usage"] = {}
    coupon["user_usage"][user_id] = coupon["user_usage"].get(user_id, 0) + 1
    coupon["remaining_count"] -= 1
    
    # 记录使用历史
    usage_key = f"{user_id}_{order_id}"
    if usage_key not in POINTS_HISTORY:
        POINTS_HISTORY[usage_key] = []
    POINTS_HISTORY[usage_key].append({
        "type": "coupon_redeem",
        "coupon_code": code,
        "used_at": datetime.now().isoformat(),
        "order_id": order_id
    })
    
    return json.dumps({
        "success": True,
        "message": "Coupon redeemed successfully",
        "coupon_code": code,
        "remaining_uses": coupon["user_limit"] - coupon["user_usage"].get(user_id, 0)
    })

@tool
def create_coupon(merchant_id: str, coupon_data: str) -> str:
    """商家创建优惠券"""
    try:
        data = json.loads(coupon_data)
    except:
        return json.dumps({"success": False, "error": "Invalid coupon data"})
    
    code = data["code"].upper()
    now = datetime.now()
    
    if code in COUPONS:
        return json.dumps({"success": False, "error": "Coupon code already exists"})
    
    coupon = {
        "code": code,
        "merchant_id": merchant_id,
        "name": data["name"],
        "description": data.get("description", ""),
        "discount_type": data.get("discount_type", "fixed"),
        "discount_value": data["discount_value"],
        "min_order_cents": data.get("min_order_cents", 0),
        "max_discount_cents": data.get("max_discount_cents", 0),
        "status": "active",
        "valid_from": data.get("valid_from", now.isoformat()),
        "valid_until": data.get("valid_until", (now + timedelta(days=30)).isoformat()),
        "total_count": data.get("total_count", 100),
        "remaining_count": data.get("total_count", 100),
        "user_limit": data.get("user_limit", 1),
        "applicable_categories": data.get("categories", []),
        "created_at": now.isoformat()
    }
    
    COUPONS[code] = coupon
    
    return json.dumps({
        "success": True,
        "coupon_code": code,
        "message": "Coupon created successfully"
    })

# ==================== 积分系统模块 ====================

# 积分规则
POINTS_RULES = {
    "signup": 100,              # 注册
    "first_order": 200,        # 首单
    "order": 10,               # 每消费R1得10积分
    "review": 50,              # 评价
    "share": 20,               # 分享
    "birthday": 500,           # 生日
}

# 积分兑换规则
POINTS_REDEMPTION = {
    1000: 1000,    # 1000积分 = R1
    5000: 5500,    # 5000积分 = R5.50 (10% bonus)
    10000: 12000,  # 10000积分 = R12 (20% bonus)
}

@tool
def get_user_points(user_id: str) -> str:
    """获取用户积分余额"""
    if user_id not in USER_POINTS:
        USER_POINTS[user_id] = {
            "balance": 0,
            "lifetime": 0,
            "tier": "BRONZE",
            "tier_points": 0
        }
    
    u = USER_POINTS[user_id]
    
    return json.dumps({
        "success": True,
        "user_id": user_id,
        "points": {
            "balance": u["balance"],
            "lifetime": u["lifetime"],
            "tier": u["tier"],
            "tier_name": _get_tier_name(u["tier"]),
            "next_tier": _get_next_tier(u["tier"]),
            "points_to_next_tier": _get_points_to_next_tier(u["lifetime"])
        }
    })

def _get_tier_name(tier: str) -> str:
    tiers = {"BRONZE": "Bronze Member", "SILVER": "Silver Member", "GOLD": "Gold Member", "PLATINUM": "Platinum Member"}
    return tiers.get(tier, tier)

def _get_next_tier(tier: str) -> Optional[str]:
    order = ["BRONZE", "SILVER", "GOLD", "PLATINUM"]
    try:
        idx = order.index(tier)
        return order[idx + 1] if idx < len(order) - 1 else None
    except:
        return "SILVER"

def _get_points_to_next_tier(lifetime: int) -> int:
    thresholds = {"BRONZE": 1000, "SILVER": 5000, "GOLD": 20000, "PLATINUM": 100000}
    tier = "BRONZE"
    for t, threshold in thresholds.items():
        if lifetime >= threshold:
            tier = t
    next_t = _get_next_tier(tier)
    if next_t:
        return thresholds.get(next_t, 100000) - lifetime
    return 0

def _update_tier(user_id: str):
    """更新用户等级"""
    lifetime = USER_POINTS[user_id]["lifetime"]
    if lifetime >= 100000:
        USER_POINTS[user_id]["tier"] = "PLATINUM"
    elif lifetime >= 20000:
        USER_POINTS[user_id]["tier"] = "GOLD"
    elif lifetime >= 5000:
        USER_POINTS[user_id]["tier"] = "SILVER"
    else:
        USER_POINTS[user_id]["tier"] = "BRONZE"

@tool
def earn_points(user_id: str, action: str, **kwargs) -> str:
    """
    获取积分
    
    参数:
        user_id: 用户ID
        action: 操作类型 (signup/first_order/order/review/share/birthday)
        order_amount_cents: 订单金额（用于order类型）
        order_id: 订单ID（可选）
    """
    if user_id not in USER_POINTS:
        USER_POINTS[user_id] = {"balance": 0, "lifetime": 0, "tier": "BRONZE", "tier_points": 0}
    
    points = POINTS_RULES.get(action, 0)
    
    # 订单积分：每R1得10积分
    if action == "order" and "order_amount_cents" in kwargs:
        points = kwargs["order_amount_cents"] // 100 * 10
    
    # 检查首单
    if action == "first_order":
        has_previous = any(h["type"] == "first_order" for h in POINTS_HISTORY.get(user_id, []))
        if has_previous:
            return json.dumps({"success": False, "error": "First order bonus already claimed"})
    
    if points <= 0:
        return json.dumps({"success": False, "error": "Invalid action or no points earned"})
    
    # 添加积分
    USER_POINTS[user_id]["balance"] += points
    USER_POINTS[user_id]["lifetime"] += points
    
    # 更新等级
    _update_tier(user_id)
    
    # 记录历史
    if user_id not in POINTS_HISTORY:
        POINTS_HISTORY[user_id] = []
    POINTS_HISTORY[user_id].append({
        "type": action,
        "points": points,
        "balance_after": USER_POINTS[user_id]["balance"],
        "timestamp": datetime.now().isoformat(),
        "order_id": kwargs.get("order_id", "")
    })
    
    tier = USER_POINTS[user_id]["tier"]
    
    return json.dumps({
        "success": True,
        "points_earned": points,
        "new_balance": USER_POINTS[user_id]["balance"],
        "lifetime_points": USER_POINTS[user_id]["lifetime"],
        "current_tier": tier,
        "tier_name": _get_tier_name(tier)
    })

@tool
def redeem_points(user_id: str, points_to_redeem: int) -> str:
    """
    兑换积分为优惠券
    
    参数:
        user_id: 用户ID
        points_to_redeem: 兑换积分数
    """
    if user_id not in USER_POINTS:
        return json.dumps({"success": False, "error": "User not found"})
    
    if USER_POINTS[user_id]["balance"] < points_to_redeem:
        return json.dumps({
            "success": False,
            "error": "Insufficient points",
            "available": USER_POINTS[user_id]["balance"],
            "requested": points_to_redeem
        })
    
    # 找到最合适的兑换规则
    redeem_value = 0
    used_key = 0
    for key, value in sorted(POINTS_REDEMPTION.items(), reverse=True):
        if points_to_redeem >= key:
            redeem_value = value
            used_key = key
            break
    
    if redeem_value == 0:
        return json.dumps({
            "success": False,
            "error": "Minimum 1000 points required for redemption"
        })
    
    # 扣除积分
    USER_POINTS[user_id]["balance"] -= points_to_redeem
    
    # 生成优惠码
    voucher_code = f"VCH{hash(str(user_id) + str(points_to_redeem)) % 100000000:08d}"
    now = datetime.now()
    
    # 创建优惠券
    COUPONS[voucher_code] = {
        "code": voucher_code,
        "name": f"Points Redemption",
        "description": f"Redeemed from {points_to_redeem} points",
        "discount_type": "fixed",
        "discount_value": redeem_value,
        "min_order_cents": 0,
        "max_discount_cents": redeem_value,
        "status": "active",
        "valid_from": now.isoformat(),
        "valid_until": (now + timedelta(days=30)).isoformat(),
        "total_count": 1,
        "remaining_count": 1,
        "user_limit": 1,
        "from_points": points_to_redeem
    }
    
    # 记录历史
    POINTS_HISTORY[user_id].append({
        "type": "redeem",
        "points": -points_to_redeem,
        "voucher_code": voucher_code,
        "voucher_value": redeem_value,
        "balance_after": USER_POINTS[user_id]["balance"],
        "timestamp": now.isoformat()
    })
    
    return json.dumps({
        "success": True,
        "points_redeemed": points_to_redeem,
        "voucher_code": voucher_code,
        "voucher_value": f"R{redeem_value/100:.2f}",
        "remaining_points": USER_POINTS[user_id]["balance"],
        "valid_until": (now + timedelta(days=30)).strftime("%Y-%m-%d")
    })

@tool
def get_points_history(user_id: str, limit: int = 20) -> str:
    """获取积分历史"""
    history = POINTS_HISTORY.get(user_id, [])
    history.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return json.dumps({
        "success": True,
        "user_id": user_id,
        "current_balance": USER_POINTS.get(user_id, {}).get("balance", 0),
        "count": len(history[:limit]),
        "history": [
            {
                "type": h["type"],
                "points": h["points"],
                "description": _get_points_description(h["type"]),
                "timestamp": h["timestamp"],
                "order_id": h.get("order_id", "")
            }
            for h in history[:limit]
        ]
    })

def _get_points_description(action: str) -> str:
    descriptions = {
        "signup": "Sign up bonus",
        "first_order": "First order bonus",
        "order": "Order points",
        "review": "Product review",
        "share": "Share reward",
        "birthday": "Birthday bonus",
        "redeem": "Points redemption"
    }
    return descriptions.get(action, action)

@tool
def get_points_exchange_rates() -> str:
    """获取积分兑换规则"""
    return json.dumps({
        "success": True,
        "rules": [
            {"points": key, "reward": f"R{value/100:.2f}", "bonus": f"+{value-key} pts" if value > key else ""}
            for key, value in POINTS_REDEMPTION.items()
        ],
        "earn_rules": [
            {"action": k, "points": v, "description": _get_points_description(k)}
            for k, v in POINTS_RULES.items()
        ]
    })

@tool
def get_tier_benefits() -> str:
    """获取会员等级权益"""
    benefits = {
        "BRONZE": {
            "name": "Bronze Member",
            "min_points": 0,
            "discount": "0%",
            "free_shipping_threshold": 50000,
            "birthday_bonus": 500,
            "exclusive_access": False
        },
        "SILVER": {
            "name": "Silver Member",
            "min_points": 5000,
            "discount": "2%",
            "free_shipping_threshold": 40000,
            "birthday_bonus": 1000,
            "exclusive_access": False
        },
        "GOLD": {
            "name": "Gold Member",
            "min_points": 20000,
            "discount": "5%",
            "free_shipping_threshold": 30000,
            "birthday_bonus": 2000,
            "exclusive_access": True
        },
        "PLATINUM": {
            "name": "Platinum Member",
            "min_points": 100000,
            "discount": "10%",
            "free_shipping_threshold": 0,
            "birthday_bonus": 5000,
            "exclusive_access": True,
            "priority_support": True
        }
    }
    
    return json.dumps({
        "success": True,
        "tiers": benefits
    })
