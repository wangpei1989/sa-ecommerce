"""
商品管理工具
提供商品搜索、详情查看、分类浏览功能
"""
import json
from typing import Optional, List, Dict, Any
from langchain.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context

# 商品数据存储（实际项目中应连接数据库）
# 当前为演示数据结构
PRODUCT_DB: Dict[str, Any] = {
    "SKU001": {
        "sku_id": "SKU001",
        "name": "Wireless Bluetooth Headphones",
        "name_zh": "无线蓝牙耳机",
        "description": "High-quality wireless headphones with noise cancellation",
        "price": 29900,  # 单位: 分 (299 ZAR)
        "stock": 150,
        "category": "Electronics",
        "images": ["https://cdn.example.com/headphones.jpg"],
        "weight": 0.25,  # kg
        "shipping_fee": 5000,  # 分 (50 ZAR)
    },
    "SKU002": {
        "sku_id": "SKU002",
        "name": "Smart Watch Pro",
        "name_zh": "智能手表 Pro",
        "description": "Advanced smartwatch with health monitoring",
        "price": 59900,  # 单位: 分
        "stock": 80,
        "category": "Electronics",
        "images": ["https://cdn.example.com/smartwatch.jpg"],
        "weight": 0.08,
        "shipping_fee": 5000,
    },
    "SKU003": {
        "sku_id": "SKU003",
        "name": "Cotton T-Shirt",
        "name_zh": "纯棉T恤",
        "description": "Comfortable 100% cotton t-shirt",
        "price": 8900,
        "stock": 500,
        "category": "Clothing",
        "images": ["https://cdn.example.com/tshirt.jpg"],
        "weight": 0.2,
        "shipping_fee": 3000,
    },
}


@tool
def search_product(
    keyword: str,
    category: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    limit: int = 10
) -> str:
    """
    搜索商品
    
    Args:
        keyword: 搜索关键词
        category: 商品分类(可选)
        min_price: 最低价格，单位分(可选)
        max_price: 最高价格，单位分(可选)
        limit: 返回数量限制，默认10
        
    Returns:
        商品列表JSON
    """
    ctx = request_context.get() or new_context(method="search_product")
    
    results = []
    for sku_id, product in PRODUCT_DB.items():
        # 关键词匹配
        if keyword.lower() in product["name"].lower() or keyword.lower() in product["name_zh"].lower():
            # 分类过滤
            if category and product["category"] != category:
                continue
            # 价格过滤
            if min_price and product["price"] < min_price:
                continue
            if max_price and product["price"] > max_price:
                continue
            # 库存过滤
            if product["stock"] <= 0:
                continue
            results.append(product)
    
    # 限制返回数量
    results = results[:limit]
    
    return json.dumps({
        "success": True,
        "count": len(results),
        "products": results
    }, ensure_ascii=False)


@tool
def get_product_detail(sku_id: str) -> str:
    """
    获取商品详情
    
    Args:
        sku_id: 商品SKU编号
        
    Returns:
        商品详情JSON
    """
    ctx = request_context.get() or new_context(method="get_product_detail")
    
    product = PRODUCT_DB.get(sku_id)
    if not product:
        return json.dumps({
            "success": False,
            "error": f"Product {sku_id} not found"
        })
    
    return json.dumps({
        "success": True,
        "product": product
    }, ensure_ascii=False)


@tool
def get_categories() -> str:
    """
    获取所有商品分类
    
    Returns:
        分类列表JSON
    """
    categories = list(set(p["category"] for p in PRODUCT_DB.values()))
    return json.dumps({
        "success": True,
        "categories": categories
    })
