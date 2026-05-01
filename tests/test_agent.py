"""
南非跨境电商 Agent 测试用例
"""
import pytest
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestProductTool:
    """商品工具测试"""
    
    def test_search_product(self):
        from tools.product_tool import search_product
        result = search_product.invoke({"keyword": "headphone"})
        data = eval(result) if isinstance(result, str) else result
        
        assert data["success"] == True
        assert data["count"] >= 1
        assert "products" in data
    
    def test_get_product_detail(self):
        from tools.product_tool import get_product_detail
        result = get_product_detail.invoke({"sku_id": "SKU001"})
        data = eval(result) if isinstance(result, str) else result
        
        assert data["success"] == True
        assert data["product"]["sku_id"] == "SKU001"
    
    def test_get_categories(self):
        from tools.product_tool import get_categories
        result = get_categories.invoke({})
        data = eval(result) if isinstance(result, str) else result
        
        assert data["success"] == True
        assert len(data["categories"]) > 0


class TestOrderTool:
    """订单工具测试"""
    
    def test_create_order(self):
        from tools.order_tool import create_order
        
        shipping_address = {
            "name": "Test User",
            "phone": "+27123456789",
            "province": "Gauteng",
            "city": "Johannesburg",
            "address": "123 Main Street",
            "postal_code": "2000"
        }
        
        result = create_order.invoke({
            "user_id": "TEST001",
            "sku_id": "SKU001",
            "quantity": 1,
            "shipping_address": shipping_address
        })
        data = eval(result) if isinstance(result, str) else result
        
        assert data["success"] == True
        assert "order_id" in data["order"]
        assert data["order"]["status"] == "pending"
    
    def test_get_order_status(self):
        from tools.order_tool import create_order, get_order_status
        
        # 先创建订单
        shipping_address = {
            "name": "Test User",
            "phone": "+27123456789",
            "province": "Gauteng",
            "city": "Johannesburg",
            "address": "123 Main Street",
            "postal_code": "2000"
        }
        
        create_result = create_order.invoke({
            "user_id": "TEST002",
            "sku_id": "SKU002",
            "quantity": 1,
            "shipping_address": shipping_address
        })
        order_data = eval(create_result) if isinstance(create_result, str) else create_result
        order_id = order_data["order"]["order_id"]
        
        # 查询状态
        result = get_order_status.invoke({"order_id": order_id})
        data = eval(result) if isinstance(result, str) else result
        
        assert data["success"] == True
        assert data["order"]["order_id"] == order_id


class TestZARCurrency:
    """南非货币工具测试"""
    
    def test_convert_to_zar(self):
        from tools.zar_currency import convert_to_zar
        
        result = convert_to_zar.invoke({"amount": 100, "from_currency": "USD"})
        data = eval(result) if isinstance(result, str) else result
        
        assert data["success"] == True
        assert data["zar_amount"] == 100 * 18.50
    
    def test_format_zar_price(self):
        from tools.zar_currency import format_zar_price
        
        result = format_zar_price.invoke({"amount_cents": 29900})
        assert result == "R299.00"
    
    def test_validate_sa_phone(self):
        from tools.zar_currency import validate_sa_phone
        
        result = validate_sa_phone.invoke({"phone": "+27831234567"})
        data = eval(result) if isinstance(result, str) else result
        
        assert data["success"] == True
        assert data["is_valid"] == True


class TestPromotionTool:
    """营销工具测试"""
    
    def test_get_active_promotions(self):
        from tools.promotion_tool import get_active_promotions
        
        result = get_active_promotions.invoke({})
        data = eval(result) if isinstance(result, str) else result
        
        assert data["success"] == True
        assert len(data["promotions"]) > 0
    
    def test_validate_coupon(self):
        from tools.promotion_tool import validate_coupon
        
        result = validate_coupon.invoke({
            "order_amount": 20000,
            "coupon_code": "WELCOME10"
        })
        data = eval(result) if isinstance(result, str) else result
        
        assert data["success"] == True
        assert data["discount"] > 0


class TestShippingTool:
    """物流工具测试"""
    
    def test_calculate_shipping_fee(self):
        from tools.shipping_tool import calculate_shipping_fee
        
        result = calculate_shipping_fee.invoke({
            "weight": 0.5,
            "province": "Gauteng",
            "is_express": False
        })
        data = eval(result) if isinstance(result, str) else result
        
        assert data["success"] == True
        assert data["total_fee"] > 0
    
    def test_get_pickup_points(self):
        from tools.shipping_tool import get_pickup_points
        
        result = get_pickup_points.invoke({"city": "Johannesburg"})
        data = eval(result) if isinstance(result, str) else result
        
        assert data["success"] == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
