"""南非跨境电商核心工具集"""
import json
import re
from datetime import datetime
from langchain.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context

def _ctx():
    """获取请求上下文"""
    return request_context.get() or new_context(method="ecommerce")

def _fmt(cents: int) -> str:
    """分转ZAR格式"""
    return f"R{cents / 100:.2f}"

# ==================== 用户认证模块 ====================

VERIFICATION_CODES = {}

@tool
def send_sms_code(phone: str) -> str:
    """发送手机验证码"""
    _ctx()
    if not re.match(r'^\+27[1-9]\d{8}$', phone):
        return json.dumps({"success": False, "error": "Invalid SA phone number"})
    code = str(111111)
    VERIFICATION_CODES[phone] = code
    return json.dumps({"success": True, "message": f"Code sent to {phone}", "code": code})

@tool
def register_user(phone: str, code: str, name: str = "") -> str:
    """注册用户"""
    _ctx()
    if VERIFICATION_CODES.get(phone) != code:
        return json.dumps({"success": False, "error": "Invalid verification code"})
    user_id = f"USER{hash(phone) % 100000:05d}"
    return json.dumps({"success": True, "user_id": user_id, "message": "Registration successful"})

@tool
def login_user(phone: str, code: str) -> str:
    """用户登录"""
    _ctx()
    if VERIFICATION_CODES.get(phone) != code:
        return json.dumps({"success": False, "error": "Invalid verification code"})
    user_id = f"USER{hash(phone) % 100000:05d}"
    return json.dumps({"success": True, "user_id": user_id, "token": "mock_token"})

@tool
def get_user_profile(user_id: str) -> str:
    """获取用户信息"""
    _ctx()
    return json.dumps({
        "success": True,
        "user": {"user_id": user_id, "name": "User", "tier": "BRONZE", "points": 0}
    })

# ==================== 商品模块 ====================

PRODUCTS = [
    {"sku_id": "SKU001", "name": "Wireless Bluetooth Headphones", "price": 29900, "stock": 150, "category": "Electronics"},
    {"sku_id": "SKU002", "name": "Rooibos Tea Gift Box", "price": 8900, "stock": 200, "category": "Local Specialties"},
    {"sku_id": "SKU003", "name": "Smart Watch Pro", "price": 59900, "stock": 80, "category": "Electronics"},
    {"sku_id": "SKU004", "name": "South African Honey", "price": 4500, "stock": 300, "category": "Local Specialties"},
    {"sku_id": "SKU005", "name": "Yoga Mat Premium", "price": 19900, "stock": 100, "category": "Sports"},
]

@tool
def search_products(keyword: str = "", category: str = "") -> str:
    """搜索商品"""
    _ctx()
    results = [p for p in PRODUCTS if keyword.lower() in p["name"].lower() or not keyword]
    if category:
        results = [p for p in results if p["category"] == category]
    for p in results:
        p["price_display"] = _fmt(p["price"])
    return json.dumps({"success": True, "products": results, "count": len(results)})

@tool
def get_product_detail(sku_id: str) -> str:
    """获取商品详情"""
    _ctx()
    for p in PRODUCTS:
        if p["sku_id"] == sku_id:
            result = dict(p)
            result["price_display"] = _fmt(p["price"])
            return json.dumps({"success": True, "product": result})
    return json.dumps({"success": False, "error": "Product not found"})

@tool
def get_categories() -> str:
    """获取商品分类"""
    return json.dumps({"success": True, "categories": ["Electronics", "Fashion", "Home", "Local Specialties", "Beauty", "Sports"]})

# ==================== 购物车模块 ====================

CARTS = {}

@tool
def add_to_cart(user_id: str, sku_id: str, quantity: int = 1) -> str:
    """添加商品到购物车"""
    _ctx()
    if user_id not in CARTS:
        CARTS[user_id] = {}
    CARTS[user_id][sku_id] = CARTS[user_id].get(sku_id, 0) + quantity
    return json.dumps({"success": True, "message": "Added to cart"})

@tool
def get_cart(user_id: str) -> str:
    """获取购物车"""
    _ctx()
    items = [{"sku_id": k, "quantity": v} for k, v in CARTS.get(user_id, {}).items()]
    return json.dumps({"success": True, "items": items, "count": len(items)})

@tool
def remove_from_cart(user_id: str, sku_id: str) -> str:
    """移除购物车商品"""
    _ctx()
    if user_id in CARTS and sku_id in CARTS[user_id]:
        del CARTS[user_id][sku_id]
    return json.dumps({"success": True, "message": "Removed from cart"})

# ==================== 物流模块 ====================

PROVINCES = {"GP": "Gauteng", "WC": "Western Cape", "KZN": "KwaZulu-Natal"}

@tool
def get_provinces() -> str:
    """获取南非省份"""
    return json.dumps({"success": True, "provinces": PROVINCES})

@tool
def add_shipping_address(user_id: str, province: str, city: str, address: str, postal_code: str, name: str = "", phone: str = "") -> str:
    """添加收货地址"""
    _ctx()
    addr_id = f"ADDR{hash(address) % 100000:08X}"
    return json.dumps({"success": True, "address_id": addr_id})

@tool
def get_shipping_addresses(user_id: str) -> str:
    """获取收货地址列表"""
    return json.dumps({"success": True, "addresses": []})

# ==================== 订单模块 ====================

ORDERS = {}

@tool
def create_order(user_id: str, items: str, shipping_address_id: str, payment_method: str = "CARD") -> str:
    """创建订单"""
    _ctx()
    order_id = f"ORD{datetime.now().strftime('%Y%m%d')}{hash(user_id) % 10000:04X}"
    total = 29900
    ORDERS[order_id] = {"order_id": order_id, "user_id": user_id, "status": "pending", "total": total}
    return json.dumps({
        "success": True, "order_id": order_id,
        "payment_url": f"https://pay.example.com/{order_id}",
        "total_display": _fmt(total)
    })

@tool
def get_order_list(user_id: str) -> str:
    """获取订单列表"""
    user_orders = [o for o in ORDERS.values() if o["user_id"] == user_id]
    return json.dumps({"success": True, "orders": user_orders})

@tool
def get_order_detail(order_id: str) -> str:
    """获取订单详情"""
    if order_id in ORDERS:
        return json.dumps({"success": True, "order": ORDERS[order_id]})
    return json.dumps({"success": False, "error": "Order not found"})

@tool
def cancel_order(order_id: str, user_id: str) -> str:
    """取消订单"""
    if order_id in ORDERS and ORDERS[order_id]["user_id"] == user_id:
        ORDERS[order_id]["status"] = "cancelled"
        return json.dumps({"success": True, "message": "Order cancelled"})
    return json.dumps({"success": False, "error": "Cannot cancel order"})

# ==================== 支付模块 ====================

PAYMENTS = {}

@tool
def get_payment_methods() -> str:
    """获取支付方式"""
    return json.dumps({
        "success": True,
        "methods": [
            {"id": "CARD", "name": "Credit/Debit Card", "fee": "2.5%"},
            {"id": "EFT", "name": "Instant EFT", "fee": "Free"},
            {"id": "OZOW", "name": "Ozow", "fee": "Free"},
            {"id": "PAYPAL", "name": "PayPal", "fee": "3.5%"}
        ]
    })

@tool
def initiate_payment(order_id: str, method: str) -> str:
    """发起支付"""
    _ctx()
    pay_id = f"PAY{hash(order_id) % 1000000000:010X}"
    PAYMENTS[pay_id] = {"pay_id": pay_id, "order_id": order_id, "status": "pending"}
    return json.dumps({
        "success": True, "payment_id": pay_id,
        "payment_url": f"https://pay.example.com/{pay_id}"
    })

@tool
def get_payment_status(payment_id: str) -> str:
    """查询支付状态"""
    if payment_id in PAYMENTS:
        return json.dumps({"success": True, "status": PAYMENTS[payment_id]["status"]})
    return json.dumps({"success": False, "error": "Payment not found"})

# ==================== 售后模块 ====================

@tool
def apply_refund(order_id: str, reason: str) -> str:
    """申请退款"""
    return json.dumps({"success": True, "refund_id": f"REF{hash(order_id) % 100000:08X}"})

@tool
def get_refund_list(user_id: str) -> str:
    """获取退款列表"""
    return json.dumps({"success": True, "refunds": []})

@tool
def confirm_delivery(order_id: str) -> str:
    """确认收货"""
    if order_id in ORDERS:
        ORDERS[order_id]["status"] = "completed"
        return json.dumps({"success": True})
    return json.dumps({"success": False})
