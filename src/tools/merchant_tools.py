"""
南非跨境电商 - 商家端核心功能
包含：店铺入驻、商品上架、订单处理、售后管理、对账结算
"""
import json
import re
from datetime import datetime, timedelta
from typing import Optional, List
from langchain.tools import tool

# ==================== 数据存储（模拟数据库） ====================

# 商家店铺数据
MERCHANTS = {}

# 商品数据
PRODUCTS = {}

# 商家订单
MERCHANT_ORDERS = {}

# 售后工单
AFTER_SALES = {}

# 对账单
STATEMENTS = {}

# ==================== 店铺入驻模块 ====================

# 商家类型
MERCHANT_TYPES = {
    "local": "Local SA Business",
    "cross_border": "Cross-Border Seller",
    "verified": "Verified International Brand"
}

# 入驻状态
MERCHANT_STATUS = {
    "pending": "Pending Review",
    "approved": "Approved",
    "rejected": "Rejected",
    "suspended": "Suspended"
}

@tool
def register_merchant(
    merchant_name: str,
    business_type: str,
    registration_number: str,
    contact_email: str,
    contact_phone: str,
    bank_account: str,
    bank_name: str
) -> str:
    """
    商家入驻申请
    
    参数:
        merchant_name: 商家名称
        business_type: 商家类型 (local/cross_border/verified)
        registration_number: 营业执照号
        contact_email: 联系邮箱
        contact_phone: 联系电话
        bank_account: 银行账号
        bank_name: 银行名称
    """
    # 验证营业执照号格式（南非公司注册号）
    if not re.match(r'^[A-Z0-9]{4,18}$', registration_number.upper()):
        return json.dumps({
            "success": False,
            "error": "Invalid registration number format",
            "hint": "South African registration number: 4-18 alphanumeric characters"
        })
    
    # 验证邮箱格式
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', contact_email):
        return json.dumps({
            "success": False,
            "error": "Invalid email format"
        })
    
    # 验证手机号
    phone_clean = re.sub(r'[\s\-\(\)]', '', contact_phone)
    if not (phone_clean.startswith('+27') and len(phone_clean) == 12) and \
       not (phone_clean.startswith('0') and len(phone_clean) == 10):
        return json.dumps({
            "success": False,
            "error": "Invalid SA phone number"
        })
    
    # 生成商家ID
    merchant_id = f"MER{hash(registration_number) % 100000000:08d}"
    now = datetime.now()
    
    merchant = {
        "merchant_id": merchant_id,
        "merchant_name": merchant_name,
        "business_type": business_type,
        "business_type_name": MERCHANT_TYPES.get(business_type, business_type),
        "registration_number": registration_number.upper(),
        "contact_email": contact_email,
        "contact_phone": phone_clean,
        "bank_account": bank_account,
        "bank_name": bank_name,
        "status": "approved",  # 模拟：直接通过
        "created_at": now.isoformat(),
        "verified_at": now.isoformat(),
        "rating": 0.0,
        "total_orders": 0,
        "total_sales_cents": 0
    }
    
    MERCHANTS[merchant_id] = merchant
    
    return json.dumps({
        "success": True,
        "merchant_id": merchant_id,
        "status": "approved",
        "message": "Merchant registration approved",
        "merchant": {
            "merchant_id": merchant_id,
            "merchant_name": merchant_name,
            "business_type": MERCHANT_TYPES.get(business_type, business_type),
            "created_at": now.strftime("%Y-%m-%d %H:%M:%S")
        }
    })

@tool
def get_merchant_profile(merchant_id: str) -> str:
    """获取商家店铺信息"""
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Merchant not found"})
    
    m = MERCHANTS[merchant_id]
    return json.dumps({
        "success": True,
        "merchant": {
            "merchant_id": m["merchant_id"],
            "merchant_name": m["merchant_name"],
            "business_type": m["business_type"],
            "business_type_name": m["business_type_name"],
            "status": m["status"],
            "rating": m["rating"],
            "total_orders": m["total_orders"],
            "total_sales": f"R{m['total_sales_cents']/100:,.2f}",
            "created_at": m["created_at"],
            "verified_at": m["verified_at"]
        }
    })

@tool
def update_merchant_info(merchant_id: str, **kwargs) -> str:
    """更新商家信息"""
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Merchant not found"})
    
    allowed_fields = ["merchant_name", "contact_email", "contact_phone", "bank_account", "bank_name"]
    for key, value in kwargs.items():
        if key in allowed_fields:
            MERCHANTS[merchant_id][key] = value
    
    MERCHANTS[merchant_id]["updated_at"] = datetime.now().isoformat()
    
    return json.dumps({
        "success": True,
        "message": "Merchant info updated",
        "merchant_id": merchant_id
    })

@tool
def get_merchant_status(merchant_id: str) -> str:
    """获取商家运营状态"""
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Merchant not found"})
    
    m = MERCHANTS[merchant_id]
    
    # 统计数据
    pending_orders = sum(1 for o in MERCHANT_ORDERS.values() 
                        if o.get("merchant_id") == merchant_id and o["status"] == "pending")
    processing_orders = sum(1 for o in MERCHANT_ORDERS.values() 
                           if o.get("merchant_id") == merchant_id and o["status"] == "processing")
    pending_after_sales = sum(1 for a in AFTER_SALES.values() 
                             if a.get("merchant_id") == merchant_id and a["status"] == "pending")
    
    return json.dumps({
        "success": True,
        "merchant_id": merchant_id,
        "status": m["status"],
        "today_stats": {
            "new_orders": pending_orders,
            "processing_orders": processing_orders,
            "pending_after_sales": pending_after_sales,
            "total_revenue_today": f"R{MERCHANTS[merchant_id].get('today_revenue', 0)/100:.2f}"
        },
        "overall_stats": {
            "total_orders": m["total_orders"],
            "total_sales": f"R{m['total_sales_cents']/100:,.2f}",
            "rating": m["rating"]
        }
    })

# ==================== 商品上架模块 ====================

# 商品状态
PRODUCT_STATUS = {
    "active": "Active",
    "inactive": "Inactive",
    "pending_review": "Pending Review",
    "rejected": "Rejected",
    "out_of_stock": "Out of Stock"
}

# 商品类别
PRODUCT_CATEGORIES = [
    "Electronics", "Fashion", "Home & Living", "Beauty", 
    "Sports", "Toys", "Food", "Books", "Automotive"
]

@tool
def list_product(merchant_id: str, product_data: str) -> str:
    """
    商品上架
    
    参数:
        merchant_id: 商家ID
        product_data: 商品信息 (JSON字符串)
            - name: 商品名称
            - description: 商品描述
            - category: 商品类目
            - price_cents: 价格（分）
            - stock: 库存数量
            - sku: SKU编号
    """
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Invalid merchant"})
    
    try:
        data = json.loads(product_data)
    except:
        return json.dumps({"success": False, "error": "Invalid product data format"})
    
    # 验证必填字段
    required = ["name", "category", "price_cents", "stock"]
    for field in required:
        if field not in data:
            return json.dumps({"success": False, "error": f"Missing required field: {field}"})
    
    # 生成商品ID
    product_id = f"PRD{hash(data.get('sku', data['name'])) % 100000000:08d}"
    now = datetime.now()
    
    product = {
        "product_id": product_id,
        "merchant_id": merchant_id,
        "sku": data.get("sku", f"SKU{product_id}"),
        "name": data["name"],
        "description": data.get("description", ""),
        "category": data["category"],
        "price_cents": data["price_cents"],
        "price_display": f"R{data['price_cents']/100:.2f}",
        "stock": data["stock"],
        "status": "active",
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "sales_count": 0
    }
    
    PRODUCTS[product_id] = product
    
    return json.dumps({
        "success": True,
        "product_id": product_id,
        "sku": product["sku"],
        "status": "active",
        "message": "Product listed successfully",
        "product": {
            "product_id": product_id,
            "name": product["name"],
            "price": product["price_display"],
            "stock": product["stock"]
        }
    })

@tool
def update_product(merchant_id: str, product_id: str, **kwargs) -> str:
    """更新商品信息"""
    if product_id not in PRODUCTS:
        return json.dumps({"success": False, "error": "Product not found"})
    
    if PRODUCTS[product_id]["merchant_id"] != merchant_id:
        return json.dumps({"success": False, "error": "Unauthorized"})
    
    allowed = ["name", "description", "category", "price_cents", "stock", "status"]
    for key, value in kwargs.items():
        if key in allowed:
            if key == "price_cents":
                PRODUCTS[product_id]["price_display"] = f"R{value/100:.2f}"
            PRODUCTS[product_id][key] = value
    
    PRODUCTS[product_id]["updated_at"] = datetime.now().isoformat()
    
    return json.dumps({
        "success": True,
        "product_id": product_id,
        "message": "Product updated"
    })

@tool
def get_merchant_products(merchant_id: str, status: str = "") -> str:
    """获取商家商品列表"""
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Invalid merchant"})
    
    products = [p for p in PRODUCTS.values() if p["merchant_id"] == merchant_id]
    
    if status:
        products = [p for p in products if p["status"] == status]
    
    return json.dumps({
        "success": True,
        "count": len(products),
        "products": [
            {
                "product_id": p["product_id"],
                "sku": p["sku"],
                "name": p["name"],
                "price": p["price_display"],
                "stock": p["stock"],
                "status": p["status"],
                "sales_count": p["sales_count"]
            }
            for p in products
        ]
    })

@tool
def update_stock(merchant_id: str, product_id: str, quantity: int) -> str:
    """更新库存"""
    if product_id not in PRODUCTS:
        return json.dumps({"success": False, "error": "Product not found"})
    
    if PRODUCTS[product_id]["merchant_id"] != merchant_id:
        return json.dumps({"success": False, "error": "Unauthorized"})
    
    PRODUCTS[product_id]["stock"] += quantity
    PRODUCTS[product_id]["updated_at"] = datetime.now().isoformat()
    
    # 检查是否缺货
    if PRODUCTS[product_id]["stock"] <= 0:
        PRODUCTS[product_id]["status"] = "out_of_stock"
    
    return json.dumps({
        "success": True,
        "product_id": product_id,
        "new_stock": PRODUCTS[product_id]["stock"],
        "status": PRODUCTS[product_id]["status"]
    })

@tool
def get_product_categories() -> str:
    """获取商品类目列表"""
    return json.dumps({
        "success": True,
        "categories": PRODUCT_CATEGORIES
    })

# ==================== 订单处理模块 ====================

# 订单状态
ORDER_STATUS = {
    "pending": "Pending",
    "confirmed": "Confirmed",
    "processing": "Processing",
    "shipped": "Shipped",
    "delivered": "Delivered",
    "cancelled": "Cancelled",
    "refunded": "Refunded"
}

@tool
def get_merchant_orders(merchant_id: str, status: str = "") -> str:
    """获取商家订单列表"""
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Invalid merchant"})
    
    orders = [o for o in MERCHANT_ORDERS.values() if o["merchant_id"] == merchant_id]
    
    if status:
        orders = [o for o in orders if o["status"] == status]
    
    # 按时间倒序
    orders.sort(key=lambda x: x["created_at"], reverse=True)
    
    return json.dumps({
        "success": True,
        "count": len(orders),
        "orders": [
            {
                "order_id": o["order_id"],
                "customer_name": o["customer_name"],
                "total_amount": f"R{o['total_cents']/100:.2f}",
                "status": o["status"],
                "created_at": o["created_at"]
            }
            for o in orders[:50]
        ]
    })

@tool
def get_order_detail(merchant_id: str, order_id: str) -> str:
    """获取订单详情"""
    if order_id not in MERCHANT_ORDERS:
        return json.dumps({"success": False, "error": "Order not found"})
    
    order = MERCHANT_ORDERS[order_id]
    if order["merchant_id"] != merchant_id:
        return json.dumps({"success": False, "error": "Unauthorized"})
    
    return json.dumps({
        "success": True,
        "order": {
            "order_id": order["order_id"],
            "customer": order["customer"],
            "items": order["items"],
            "shipping_address": order["shipping_address"],
            "total_cents": order["total_cents"],
            "total_display": f"R{order['total_cents']/100:.2f}",
            "status": order["status"],
            "created_at": order["created_at"],
            "updated_at": order["updated_at"]
        }
    })

@tool
def process_order(merchant_id: str, order_id: str, action: str) -> str:
    """
    处理订单
    
    参数:
        merchant_id: 商家ID
        order_id: 订单ID
        action: 操作 (confirm/ship/cancel)
    """
    if order_id not in MERCHANT_ORDERS:
        return json.dumps({"success": False, "error": "Order not found"})
    
    order = MERCHANT_ORDERS[order_id]
    if order["merchant_id"] != merchant_id:
        return json.dumps({"success": False, "error": "Unauthorized"})
    
    now = datetime.now().isoformat()
    
    if action == "confirm":
        if order["status"] != "pending":
            return json.dumps({"success": False, "error": "Order cannot be confirmed"})
        order["status"] = "confirmed"
        order["confirmed_at"] = now
        
    elif action == "ship":
        if order["status"] not in ["confirmed", "processing"]:
            return json.dumps({"success": False, "error": "Order cannot be shipped"})
        order["status"] = "shipped"
        order["shipped_at"] = now
        order["tracking_number"] = f"SA{hash(order_id) % 10000000000:010d}"
        
    elif action == "cancel":
        if order["status"] in ["shipped", "delivered"]:
            return json.dumps({"success": False, "error": "Cannot cancel shipped order"})
        order["status"] = "cancelled"
        order["cancelled_at"] = now
    
    order["updated_at"] = now
    
    return json.dumps({
        "success": True,
        "order_id": order_id,
        "new_status": order["status"],
        "action": action,
        "updated_at": now
    })

@tool
def batch_process_orders(merchant_id: str, order_ids: str, action: str) -> str:
    """批量处理订单"""
    try:
        order_list = json.loads(order_ids)
    except:
        return json.dumps({"success": False, "error": "Invalid order_ids format"})
    
    results = []
    for oid in order_list:
        result = json.loads(process_order(merchant_id, oid, action))
        results.append({
            "order_id": oid,
            "success": result.get("success", False),
            "error": result.get("error", "")
        })
    
    success_count = sum(1 for r in results if r["success"])
    
    return json.dumps({
        "success": True,
        "total": len(results),
        "success_count": success_count,
        "failed_count": len(results) - success_count,
        "results": results
    })

# ==================== 售后管理模块 ====================

# 售后类型
AFTER_SALES_TYPES = {
    "refund": "Refund",
    "return": "Return & Refund",
    "exchange": "Exchange",
    "complaint": "Complaint"
}

# 售后状态
AFTER_SALES_STATUS = {
    "pending": "Pending",
    "processing": "Processing",
    "approved": "Approved",
    "rejected": "Rejected",
    "completed": "Completed"
}

@tool
def get_after_sales_list(merchant_id: str, status: str = "") -> str:
    """获取售后工单列表"""
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Invalid merchant"})
    
    tickets = [a for a in AFTER_SALES.values() if a["merchant_id"] == merchant_id]
    
    if status:
        tickets = [t for t in tickets if t["status"] == status]
    
    tickets.sort(key=lambda x: x["created_at"], reverse=True)
    
    return json.dumps({
        "success": True,
        "count": len(tickets),
        "tickets": [
            {
                "ticket_id": t["ticket_id"],
                "order_id": t["order_id"],
                "type": t["type"],
                "reason": t["reason"],
                "status": t["status"],
                "created_at": t["created_at"]
            }
            for t in tickets[:30]
        ]
    })

@tool
def process_after_sales(merchant_id: str, ticket_id: str, action: str, **kwargs) -> str:
    """
    处理售后工单
    
    参数:
        merchant_id: 商家ID
        ticket_id: 工单ID
        action: 操作 (approve/reject/complete)
        **kwargs: 额外参数 (remark: 处理备注)
    """
    if ticket_id not in AFTER_SALES:
        return json.dumps({"success": False, "error": "Ticket not found"})
    
    ticket = AFTER_SALES[ticket_id]
    if ticket["merchant_id"] != merchant_id:
        return json.dumps({"success": False, "error": "Unauthorized"})
    
    now = datetime.now().isoformat()
    remark = kwargs.get("remark", "")
    
    if action == "approve":
        if ticket["status"] != "pending":
            return json.dumps({"success": False, "error": "Ticket cannot be approved"})
        ticket["status"] = "approved"
        ticket["approved_at"] = now
        ticket["merchant_remark"] = remark
        
    elif action == "reject":
        if ticket["status"] not in ["pending", "processing"]:
            return json.dumps({"success": False, "error": "Ticket cannot be rejected"})
        ticket["status"] = "rejected"
        ticket["rejected_at"] = now
        ticket["merchant_remark"] = remark
        
    elif action == "complete":
        if ticket["status"] != "approved":
            return json.dumps({"success": False, "error": "Ticket must be approved first"})
        ticket["status"] = "completed"
        ticket["completed_at"] = now
    
    ticket["updated_at"] = now
    
    return json.dumps({
        "success": True,
        "ticket_id": ticket_id,
        "new_status": ticket["status"],
        "action": action,
        "updated_at": now
    })

@tool
def get_after_sales_detail(merchant_id: str, ticket_id: str) -> str:
    """获取售后工单详情"""
    if ticket_id not in AFTER_SALES:
        return json.dumps({"success": False, "error": "Ticket not found"})
    
    ticket = AFTER_SALES[ticket_id]
    if ticket["merchant_id"] != merchant_id:
        return json.dumps({"success": False, "error": "Unauthorized"})
    
    return json.dumps({
        "success": True,
        "ticket": ticket
    })

@tool
def get_after_sales_stats(merchant_id: str) -> str:
    """获取售后统计数据"""
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Invalid merchant"})
    
    tickets = [a for a in AFTER_SALES.values() if a["merchant_id"] == merchant_id]
    
    stats = {
        "total": len(tickets),
        "pending": sum(1 for t in tickets if t["status"] == "pending"),
        "processing": sum(1 for t in tickets if t["status"] == "processing"),
        "approved": sum(1 for t in tickets if t["status"] == "approved"),
        "rejected": sum(1 for t in tickets if t["status"] == "rejected"),
        "completed": sum(1 for t in tickets if t["status"] == "completed"),
    }
    
    stats["approval_rate"] = f"{(stats['completed'] / max(stats['total'], 1) * 100):.1f}%"
    
    return json.dumps({
        "success": True,
        "merchant_id": merchant_id,
        "stats": stats
    })

# ==================== 对账结算模块 ====================

@tool
def get_settlement_summary(merchant_id: str, period: str = "monthly") -> str:
    """
    获取结算摘要
    
    参数:
        merchant_id: 商家ID
        period: 周期 (daily/weekly/monthly)
    """
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Invalid merchant"})
    
    # 模拟结算数据
    orders = [o for o in MERCHANT_ORDERS.values() 
             if o["merchant_id"] == merchant_id and o["status"] in ["delivered", "shipped"]]
    
    total_sales = sum(o["total_cents"] for o in orders)
    order_count = len(orders)
    avg_order_value = total_sales / max(order_count, 1)
    
    # 平台佣金（模拟：5-15%）
    commission_rate = 0.10
    commission = int(total_sales * commission_rate)
    net_amount = total_sales - commission
    
    return json.dumps({
        "success": True,
        "merchant_id": merchant_id,
        "period": period,
        "summary": {
            "total_orders": order_count,
            "gross_sales_cents": total_sales,
            "gross_sales_display": f"R{total_sales/100:,.2f}",
            "commission_rate": f"{commission_rate*100:.0f}%",
            "commission_cents": commission,
            "commission_display": f"R{commission/100:,.2f}",
            "net_amount_cents": net_amount,
            "net_amount_display": f"R{net_amount/100:,.2f}",
            "avg_order_value_display": f"R{avg_order_value/100:,.2f}"
        }
    })

@tool
def get_transaction_details(merchant_id: str, start_date: str = "", end_date: str = "") -> str:
    """获取交易明细"""
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Invalid merchant"})
    
    orders = [o for o in MERCHANT_ORDERS.values() 
             if o["merchant_id"] == merchant_id]
    
    transactions = []
    for o in orders:
        transactions.append({
            "transaction_id": f"TXN{hash(o['order_id']) % 100000000:08d}",
            "order_id": o["order_id"],
            "customer": o["customer_name"],
            "amount_cents": o["total_cents"],
            "amount_display": f"R{o['total_cents']/100:.2f}",
            "platform_fee_cents": int(o["total_cents"] * 0.10),
            "net_amount_cents": int(o["total_cents"] * 0.90),
            "status": o["status"],
            "created_at": o["created_at"]
        })
    
    transactions.sort(key=lambda x: x["created_at"], reverse=True)
    
    return json.dumps({
        "success": True,
        "count": len(transactions),
        "transactions": transactions[:100]
    })

@tool
def request_withdrawal(merchant_id: str, amount_cents: int) -> str:
    """申请提现"""
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Invalid merchant"})
    
    # 模拟：检查余额
    available_balance = MERCHANTS[merchant_id].get("balance_cents", 0)
    
    if amount_cents > available_balance:
        return json.dumps({
            "success": False,
            "error": "Insufficient balance",
            "available": f"R{available_balance/100:.2f}",
            "requested": f"R{amount_cents/100:.2f}"
        })
    
    withdrawal_id = f"WTH{hash(str(amount_cents) + merchant_id) % 100000000:08d}"
    now = datetime.now()
    
    withdrawal = {
        "withdrawal_id": withdrawal_id,
        "merchant_id": merchant_id,
        "amount_cents": amount_cents,
        "amount_display": f"R{amount_cents/100:.2f}",
        "status": "processing",
        "created_at": now.isoformat(),
        "estimated_arrival": (now + timedelta(days=2)).strftime("%Y-%m-%d")
    }
    
    # 模拟扣减余额
    MERCHANTS[merchant_id]["balance_cents"] = available_balance - amount_cents
    
    return json.dumps({
        "success": True,
        "withdrawal_id": withdrawal_id,
        "amount": withdrawal["amount_display"],
        "status": "processing",
        "estimated_arrival": withdrawal["estimated_arrival"],
        "remaining_balance": f"R{MERCHANTS[merchant_id]['balance_cents']/100:.2f}"
    })

@tool
def get_withdrawal_history(merchant_id: str) -> str:
    """获取提现历史"""
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Invalid merchant"})
    
    # 模拟数据
    withdrawals = [
        {
            "withdrawal_id": f"WTH{hash(merchant_id + str(i)) % 100000000:08d}",
            "amount_display": f"R{1000 + i * 500:.2f}",
            "status": "completed" if i > 0 else "processing",
            "created_at": (datetime.now() - timedelta(days=i*7)).isoformat(),
            "completed_at": (datetime.now() - timedelta(days=i*7-2)).isoformat() if i > 0 else None
        }
        for i in range(5)
    ]
    
    return json.dumps({
        "success": True,
        "count": len(withdrawals),
        "withdrawals": withdrawals
    })

@tool
def get_merchant_balance(merchant_id: str) -> str:
    """获取商家账户余额"""
    if merchant_id not in MERCHANTS:
        return json.dumps({"success": False, "error": "Invalid merchant"})
    
    m = MERCHANTS[merchant_id]
    
    # 模拟计算余额
    pending_settlement = sum(o["total_cents"] for o in MERCHANT_ORDERS.values() 
                           if o["merchant_id"] == merchant_id and o["status"] in ["shipped", "delivered"])
    completed_settlement = int(pending_settlement * 0.9)  # 扣除佣金
    
    balance = m.get("balance_cents", completed_settlement)
    
    return json.dumps({
        "success": True,
        "merchant_id": merchant_id,
        "balance": {
            "available_cents": balance,
            "available_display": f"R{balance/100:,.2f}",
            "pending_settlement_cents": pending_settlement - completed_settlement,
            "pending_settlement_display": f"R{(pending_settlement - completed_settlement)/100:,.2f}"
        }
    })

# ==================== 辅助函数 ====================

@tool
def create_merchant_order(merchant_id: str, order_data: str) -> str:
    """创建商家订单（内部使用/测试）"""
    try:
        data = json.loads(order_data)
    except:
        return json.dumps({"success": False, "error": "Invalid data"})
    
    order_id = f"ORD{hash(data.get('order_id', str(datetime.now()))) % 100000000:08d}"
    now = datetime.now()
    
    order = {
        "order_id": order_id,
        "merchant_id": merchant_id,
        "customer_name": data.get("customer_name", "Customer"),
        "customer": data.get("customer", {}),
        "items": data.get("items", []),
        "shipping_address": data.get("shipping_address", {}),
        "total_cents": data.get("total_cents", 0),
        "status": "pending",
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }
    
    MERCHANT_ORDERS[order_id] = order
    
    return json.dumps({
        "success": True,
        "order_id": order_id
    })

@tool
def create_after_sales_ticket(merchant_id: str, ticket_data: str) -> str:
    """创建售后工单（内部使用/测试）"""
    try:
        data = json.loads(ticket_data)
    except:
        return json.dumps({"success": False, "error": "Invalid data"})
    
    ticket_id = f"ASM{hash(data.get('order_id', str(datetime.now()))) % 100000000:08d}"
    now = datetime.now()
    
    ticket = {
        "ticket_id": ticket_id,
        "merchant_id": merchant_id,
        "order_id": data.get("order_id", ""),
        "type": data.get("type", "refund"),
        "reason": data.get("reason", ""),
        "description": data.get("description", ""),
        "status": "pending",
        "created_at": now.isoformat(),
        "updated_at": now.isoformat()
    }
    
    AFTER_SALES[ticket_id] = ticket
    
    return json.dumps({
        "success": True,
        "ticket_id": ticket_id
    })
