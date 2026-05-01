from coze_coding_dev_sdk.database import Base

from typing import Optional
import datetime

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Double, Float, ForeignKey, Index, Integer, Numeric, PrimaryKeyConstraint, String, Text, JSON, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import Mapped, mapped_column


class HealthCheck(Base):
    __tablename__ = 'health_check'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='health_check_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))


# ============ 南非电商平台数据表 ============

class VerificationCode(Base):
    """验证码表"""
    __tablename__ = 'verification_codes'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='verification_codes_pkey'),
        UniqueConstraint('code', 'phone', name='uq_code_phone'),
        Index('verification_codes_phone_idx', 'phone'),
        Index('verification_codes_code_idx', 'code'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, comment='手机号')
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='邮箱')
    code: Mapped[str] = mapped_column(String(10), nullable=False, comment='验证码')
    type: Mapped[str] = mapped_column(String(20), nullable=False, server_default='login', comment='类型: login/register/reset')
    used: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class User(Base):
    """用户表"""
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('phone', name='uq_users_phone'),
        UniqueConstraint('email', name='uq_users_email'),
        Index('users_phone_idx', 'phone'),
        Index('users_email_idx', 'email'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, unique=True, comment='手机号')
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, unique=True, comment='邮箱')
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False, comment='密码哈希')
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='姓名')
    language: Mapped[str] = mapped_column(String(10), nullable=False, server_default='en', comment='语言偏好')
    tier: Mapped[str] = mapped_column(String(20), nullable=False, server_default='BRONZE', comment='会员等级')
    points: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment='头像URL')
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class Category(Base):
    """商品分类表"""
    __tablename__ = 'categories'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='categories_pkey'),
        Index('categories_name_idx', 'name'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment='分类名称')
    name_zh: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='中文名称')
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='图标')
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Product(Base):
    """商品表"""
    __tablename__ = 'products'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='products_pkey'),
        UniqueConstraint('sku_id', name='uq_products_sku_id'),
        Index('products_sku_id_idx', 'sku_id'),
        Index('products_category_idx', 'category_id'),
        Index('products_price_idx', 'price'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment='SKU编号')
    name: Mapped[str] = mapped_column(String(200), nullable=False, comment='商品名称')
    name_zh: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment='中文名称')
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='商品描述')
    price: Mapped[int] = mapped_column(Integer, nullable=False, comment='价格(分)')
    original_price: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='原价(分)')
    stock: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('categories.id'), nullable=True)
    images: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment='图片URL列表')
    weight: Mapped[float] = mapped_column(Float, nullable=False, server_default=text('0'), comment='重量(kg)')
    shipping_fee: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'), comment='运费(分)')
    is_local: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'), comment='是否本地好物')
    is_cross_border: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'), comment='是否跨境商品')
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class Address(Base):
    """收货地址表"""
    __tablename__ = 'addresses'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='addresses_pkey'),
        Index('addresses_user_idx', 'user_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment='收货人姓名')
    phone: Mapped[str] = mapped_column(String(20), nullable=False, comment='联系电话')
    province: Mapped[str] = mapped_column(String(50), nullable=False, comment='省份')
    city: Mapped[str] = mapped_column(String(50), nullable=False, comment='城市')
    district: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='区县')
    address: Mapped[str] = mapped_column(String(500), nullable=False, comment='详细地址')
    postal_code: Mapped[str] = mapped_column(String(10), nullable=False, comment='邮政编码')
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class CartItem(Base):
    """购物车表"""
    __tablename__ = 'cart_items'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='cart_items_pkey'),
        UniqueConstraint('user_id', 'product_id', name='uq_cart_user_product'),
        Index('cart_items_user_idx', 'user_id'),
        Index('cart_items_product_idx', 'product_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    product_id: Mapped[str] = mapped_column(String(50), nullable=False, comment='商品SKU')
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('1'))
    selected: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class Order(Base):
    """订单表"""
    __tablename__ = 'orders'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='orders_pkey'),
        UniqueConstraint('order_id', name='uq_orders_order_id'),
        Index('orders_order_id_idx', 'order_id'),
        Index('orders_user_idx', 'user_id'),
        Index('orders_status_idx', 'status'),
        Index('orders_created_idx', 'created_at'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment='订单编号')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    subtotal: Mapped[int] = mapped_column(Integer, nullable=False, comment='商品总价(分)')
    shipping_fee: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    discount: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'), comment='优惠金额(分)')
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False, comment='订单总额(分)')
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default='PENDING', comment='订单状态')
    payment_method: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment='支付方式')
    payment_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='支付流水号')
    tracking_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='物流单号')
    shipping_address: Mapped[dict] = mapped_column(JSON, nullable=False, comment='收货地址JSON')
    coupon_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='优惠券码')
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='备注')
    pay_deadline: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    estimated_delivery: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    shipped_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    delivered_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    refund_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='退款原因')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class OrderItem(Base):
    """订单明细表"""
    __tablename__ = 'order_items'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='order_items_pkey'),
        Index('order_items_order_idx', 'order_id'),
        Index('order_items_product_idx', 'product_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[str] = mapped_column(String(50), nullable=False, comment='订单编号')
    product_id: Mapped[str] = mapped_column(String(50), nullable=False, comment='商品SKU')
    product_name: Mapped[str] = mapped_column(String(200), nullable=False, comment='商品名称')
    price: Mapped[int] = mapped_column(Integer, nullable=False, comment='购买单价(分)')
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[int] = mapped_column(Integer, nullable=False, comment='小计(分)')
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Coupon(Base):
    """优惠券表"""
    __tablename__ = 'coupons'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='coupons_pkey'),
        UniqueConstraint('code', name='uq_coupons_code'),
        Index('coupons_code_idx', 'code'),
        Index('coupons_status_idx', 'is_active'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment='优惠券码')
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment='优惠券名称')
    discount_type: Mapped[str] = mapped_column(String(20), nullable=False, comment='discount_type: fixed/percent/free_shipping')
    discount_value: Mapped[int] = mapped_column(Integer, nullable=False, comment='优惠值(分)或百分比')
    max_discount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='最高优惠(分)')
    min_order_amount: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'), comment='最低消费(分)')
    total_count: Mapped[int] = mapped_column(Integer, nullable=False, comment='总数量')
    remaining: Mapped[int] = mapped_column(Integer, nullable=False, comment='剩余数量')
    valid_from: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    valid_until: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class UserCoupon(Base):
    """用户优惠券表"""
    __tablename__ = 'user_coupons'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_coupons_pkey'),
        UniqueConstraint('user_id', 'coupon_code', name='uq_user_coupon'),
        Index('user_coupons_user_idx', 'user_id'),
        Index('user_coupons_code_idx', 'coupon_code'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    coupon_code: Mapped[str] = mapped_column(String(50), nullable=False, comment='优惠券码')
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default='AVAILABLE', comment='状态: AVAILABLE/USED/EXPIRED')
    claimed_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    used_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class Payment(Base):
    """支付记录表"""
    __tablename__ = 'payments'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='payments_pkey'),
        UniqueConstraint('payment_id', name='uq_payments_payment_id'),
        Index('payments_payment_id_idx', 'payment_id'),
        Index('payments_order_idx', 'order_id'),
        Index('payments_status_idx', 'status'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    payment_id: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment='支付流水号')
    order_id: Mapped[str] = mapped_column(String(50), nullable=False, comment='订单编号')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False, comment='支付金额(分)')
    method: Mapped[str] = mapped_column(String(20), nullable=False, comment='支付方式')
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default='PENDING', comment='支付状态')
    payment_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment='支付链接')
    callback_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, comment='回调数据')
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    paid_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class AfterSales(Base):
    """售后表"""
    __tablename__ = 'after_sales'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='after_sales_pkey'),
        UniqueConstraint('aftersales_id', name='uq_after_sales_aftersales_id'),
        Index('after_sales_aftersales_id_idx', 'aftersales_id'),
        Index('after_sales_order_idx', 'order_id'),
        Index('after_sales_user_idx', 'user_id'),
        Index('after_sales_status_idx', 'status'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    aftersales_id: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment='售后单号')
    order_id: Mapped[str] = mapped_column(String(50), nullable=False, comment='订单编号')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, comment='类型: REFUND/RETURN/EXCHANGE')
    reason: Mapped[str] = mapped_column(Text, nullable=False, comment='申请原因')
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='详细描述')
    images: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, comment='图片凭证')
    amount: Mapped[int] = mapped_column(Integer, nullable=False, comment='退款金额(分)')
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default='PENDING', comment='状态: PENDING/APPROVED/REJECTED/COMPLETED')
    admin_remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='管理员备注')
    tracking_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='退货物流')
    processed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
