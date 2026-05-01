"""
南非跨境电商 Agent - 核心入口
"""
import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from coze_coding_utils.runtime_ctx.context import default_headers
from storage.memory.memory_saver import get_memory_saver

LLM_CONFIG = "config/agent_llm_config.json"

# 滑动窗口保留最近 20 轮对话 (40 条消息)
MAX_MESSAGES = 40

def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    combined = list(add_messages(old, new))
    return combined[-MAX_MESSAGES:]

class AgentState(MessagesState):
    """Agent 状态管理，包含消息历史滑动窗口"""
    messages: Annotated[list[AnyMessage], _windowed_messages]

def build_agent(ctx=None):
    """
    构建南非电商 Agent
    
    Args:
        ctx: 请求上下文，用于链路追踪
        
    Returns:
        配置好的 Agent 实例
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    config_path = os.path.join(workspace_path, LLM_CONFIG)

    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
    base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

    llm = ChatOpenAI(
        model=cfg['config'].get("model"),
        api_key=api_key,
        base_url=base_url,
        temperature=cfg['config'].get('temperature', 0.7),
        streaming=True,
        timeout=cfg['config'].get('timeout', 600),
        extra_body={
            "thinking": {
                "type": cfg['config'].get('thinking', 'disabled')
            }
        },
        default_headers=default_headers(ctx) if ctx else {}
    )

    # 延迟导入工具，避免循环依赖
    from tools.product_tool import search_product, get_product_detail, get_categories
    from tools.order_tool import create_order, get_order_status, cancel_order, get_user_orders
    from tools.shipping_tool import track_shipment, get_pickup_points, calculate_shipping_fee
    from tools.zar_currency import convert_to_zar, format_zar_price, get_supported_languages, get_provinces, validate_sa_phone
    from tools.payment_tool import get_payment_methods, calculate_payment_fee, initiate_payment
    from tools.user_tool import get_user_profile, update_user_profile, add_shipping_address, get_shipping_addresses
    from tools.promotion_tool import get_active_promotions, claim_coupon, get_user_coupons, validate_coupon

    tools = [
        # 商品模块
        search_product,
        get_product_detail,
        get_categories,
        # 订单模块
        create_order,
        get_order_status,
        cancel_order,
        get_user_orders,
        # 物流模块
        track_shipment,
        get_pickup_points,
        calculate_shipping_fee,
        # 本地化模块
        convert_to_zar,
        format_zar_price,
        get_supported_languages,
        get_provinces,
        validate_sa_phone,
        # 支付模块
        get_payment_methods,
        calculate_payment_fee,
        initiate_payment,
        # 用户模块
        get_user_profile,
        update_user_profile,
        add_shipping_address,
        get_shipping_addresses,
        # 营销模块
        get_active_promotions,
        claim_coupon,
        get_user_coupons,
        validate_coupon,
    ]

    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=tools,
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
