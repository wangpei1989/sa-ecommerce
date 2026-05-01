"""
订单管理工具
提供订单创建、查询、取消功能
"""
import json
import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from langchain.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context

# 订单状态枚举
ORDER_STATUS = {
    "PENDING": "pending",        # 待支付
    "PAID": "paid",              # 已支付
    "PROCESSING": "processing",  # 处理中
    "SHIPPED": "shipped",       # 已发货
    "DELIVERED": "delivered",   # 已送达
    "CANCELLED": "cancelled",   # 已取消
    "REFUNDED": "refunded",     # 已退款
}

# 订单数据存储（实际项目中应连接数据库）
orders_db: Dict[str, Dict[str, Any]] = {}

# 运费规则: 超过500 ZAR(50000分)免运费
FREE_SHIPPING_THRESHOLD = 50000


@tool
def create_order(
    user_id: str,
    sku_id: str,
    quantity: int,
    shipping_address: Dict[str, str]
) -> str:
    """
    创建订单
    
    Args:
        user_id: 用户ID
        sku_id: 商品SKU编号
        quantity: 购买数量
        shipping_address: 收货地址 {"name": "姓名", "phone": "电话", "province": "省份", "city": "城市", "address": "详细地址", "postal_code": "邮编"}
        
    Returns:
        订单信息JSON
    """
    ctx = request_context.get() or new_context(method="create_order")
    
    # 获取商品信息
    from tools.product_tool import PRODUCT_DB
    product = PRODUCT_DB.get(sku_id)
    if not product:
        return json.dumps({
            "success": False,
            "error": f"Product {sku_id} not found"
        })
    
    # 检查库存
    if product["stock"] < quantity:
        return json.dumps({
            "success": False,
            "error": f"Insufficient stock. Available: {product['stock']}"
        })
    
    # 计算金额
    subtotal = product["price"] * quantity
    shipping_fee = 0 if subtotal >= FREE_SHIPPING_THRESHOLD else product["shipping_fee"]
    total_amount = subtotal + shipping_fee
    
    # 生成订单
    order_id = f"ORD{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
    now = datetime.utcnow()
    
    order = {
        "order_id": order_id,
        "user_id": user_id,
        "items": [{
            "sku_id": sku_id,
            "name": product["name"],
            "price": product["price"],
            "quantity": quantity,
            "subtotal": subtotal
        }],
        "subtotal": subtotal,
        "shipping_fee": shipping_fee,
        "total_amount": total_amount,
        "status": ORDER_STATUS["PENDING"],
        "shipping_address": shipping_address,
        "created_at": now.isoformat(),
        "pay_deadline": (now + timedelta(hours=24)).isoformat(),
        "tracking_number": None,
        "estimated_delivery": None,
    }
    
    orders_db[order_id] = order
    
    return json.dumps({
        "success": True,
        "order": order
    }, ensure_ascii=False)


@tool
def get_order_status(order_id: str) -> str:
    """
    查询订单状态
    
    Args:
        order_id: 订单编号
        
    Returns:
        订单状态JSON
    """
    ctx = request_context.get() or new_context(method="get_order_status")
    
    order = orders_db.get(order_id)
    if not order:
        return json.dumps({
            "success": False,
            "error": f"Order {order_id} not found"
        })
    
    return json.dumps({
        "success": True,
        "order": {
            "order_id": order["order_id"],
            "status": order["status"],
            "total_amount": order["total_amount"],
            "created_at": order["created_at"],
            "tracking_number": order["tracking_number"],
            "estimated_delivery": order["estimated_delivery"],
        }
    }, ensure_ascii=False)


@tool
def cancel_order(order_id: str, user_id: str) -> str:
    """
    取消订单
    
    Args:
        order_id: 订单编号
        user_id: 用户ID(用于验证)
        
    Returns:
        操作结果JSON
    """
    ctx = request_context.get() or new_context(method="cancel_order")
    
    order = orders_db.get(order_id)
    if not order:
        return json.dumps({
            "success": False,
            "error": f"Order {order_id} not found"
        })
    
    if order["user_id"] != user_id:
        return json.dumps({
            "success": False,
            "error": "Unauthorized to cancel this order"
        })
    
    if order["status"] not in [ORDER_STATUS["PENDING"], ORDER_STATUS["PAID"]]:
        return json.dumps({
            "success": False,
            "error": f"Cannot cancel order in status: {order['status']}"
        })
    
    order["status"] = ORDER_STATUS["CANCELLED"]
    
    return json.dumps({
        "success": True,
        "message": "Order cancelled successfully"
    })


@tool
def get_user_orders(user_id: str, status: Optional[str] = None, limit: int = 20) -> str:
    """
    获取用户订单列表
    
    Args:
        user_id: 用户ID
        status: 订单状态筛选(可选)
        limit: 返回数量限制
        
    Returns:
        订单列表JSON
    """
    user_orders = [o for o in orders_db.values() if o["user_id"] == user_id]
    
    if status:
        user_orders = [o for o in user_orders if o["status"] == status]
    
    # 按时间倒序
    user_orders.sort(key=lambda x: x["created_at"], reverse=True)
    user_orders = user_orders[:limit]
    
    return json.dumps({
        "success": True,
        "count": len(user_orders),
        "orders": user_orders
    })
