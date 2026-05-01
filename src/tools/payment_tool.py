"""
南非本地支付工具
支持南非本地支付方式: EFT、PayShap、Ozow等
"""
import json
from typing import Optional, Dict, Any
from langchain.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context

# 南非支付方式
PAYMENT_METHODS = {
    "CARD": {
        "id": "CARD",
        "name": "Credit/Debit Card",
        "name_zh": "信用卡/借记卡",
        "icon": "card",
        "processing_fee_rate": 0.025,  # 2.5% 手续费
    },
    "EFT": {
        "id": "EFT",
        "name": "Instant EFT",
        "name_zh": "即时电子转账",
        "icon": "eft",
        "processing_fee_rate": 0,
        "description": "Pay via your South African bank account"
    },
    "OZOW": {
        "id": "OZOW",
        "name": "Ozow Instant Payment",
        "name_zh": "Ozow即时支付",
        "icon": "ozow",
        "processing_fee_rate": 0,
        "description": "Popular instant payment method in South Africa"
    },
    "PAYPAL": {
        "id": "PAYPAL",
        "name": "PayPal",
        "name_zh": "PayPal支付",
        "icon": "paypal",
        "processing_fee_rate": 0.035,
    },
    "COD": {
        "id": "COD",
        "name": "Cash on Delivery",
        "name_zh": "货到付款",
        "icon": "cod",
        "processing_fee_rate": 0.02,
        "available": False,  # 跨境不支持
    },
}


@tool
def get_payment_methods() -> str:
    """
    获取支持的支付方式列表
    
    Returns:
        支付方式列表JSON
    """
    return json.dumps({
        "success": True,
        "payment_methods": PAYMENT_METHODS
    })


@tool
def calculate_payment_fee(amount_cents: int, method_id: str) -> str:
    """
    计算支付手续费
    
    Args:
        amount_cents: 订单金额(单位: 分)
        method_id: 支付方式ID
        
    Returns:
        手续费计算结果JSON
    """
    ctx = request_context.get() or new_context(method="calculate_payment_fee")
    
    method = PAYMENT_METHODS.get(method_id)
    if not method:
        return json.dumps({
            "success": False,
            "error": f"Unknown payment method: {method_id}"
        })
    
    fee_rate = method.get("processing_fee_rate", 0)
    fee_amount = int(amount_cents * fee_rate)
    
    return json.dumps({
        "success": True,
        "order_amount": amount_cents,
        "payment_method": method["name"],
        "fee_rate": fee_rate,
        "fee_amount": fee_amount,
        "total_amount": amount_cents + fee_amount,
        "currency": "ZAR"
    })


@tool
def initiate_payment(
    order_id: str,
    method_id: str,
    amount_cents: int,
    return_url: str
) -> str:
    """
    发起支付
    
    Args:
        order_id: 订单ID
        method_id: 支付方式ID
        amount_cents: 支付金额(单位: 分)
        return_url: 支付完成跳转URL
        
    Returns:
        支付链接JSON
    """
    ctx = request_context.get() or new_context(method="initiate_payment")
    
    method = PAYMENT_METHODS.get(method_id)
    if not method:
        return json.dumps({
            "success": False,
            "error": f"Unknown payment method: {method_id}"
        })
    
    # 模拟支付链接
    payment_id = f"PAY{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:12].upper()}"
    
    payment_urls = {
        "CARD": f"https://payments.example.com/card/{payment_id}",
        "EFT": f"https://payments.example.com/eft/{payment_id}",
        "OZOW": f"https://pay.ozow.com/{payment_id}",
        "PAYPAL": f"https://paypal.example.com/checkout/{payment_id}",
    }
    
    return json.dumps({
        "success": True,
        "payment_id": payment_id,
        "order_id": order_id,
        "amount": amount_cents,
        "method": method["name"],
        "payment_url": payment_urls.get(method_id, ""),
        "expires_in": 1800,  # 30分钟有效期
    })

import uuid
from datetime import datetime
