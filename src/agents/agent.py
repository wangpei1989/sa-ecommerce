"""
南非跨境电商Agent
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
MAX_MESSAGES = 40


def _windowed_messages(old, new):
    result = add_messages(old, new)
    return list(result)[-MAX_MESSAGES:]


class AgentState(MessagesState):
    pass


def build_agent(ctx=None):
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
        extra_body={"thinking": {"type": cfg['config'].get('thinking', 'disabled')}},
        default_headers=default_headers(ctx) if ctx else {}
    )

    from tools.ecommerce_tools import (
        send_sms_code, register_user, login_user, get_user_profile,
        search_products, get_product_detail, get_categories,
        add_to_cart, get_cart, remove_from_cart,
        get_provinces, add_shipping_address, get_shipping_addresses,
        create_order, get_order_list, get_order_detail, cancel_order,
        get_payment_methods, initiate_payment, get_payment_status,
        apply_refund, get_refund_list, confirm_delivery
    )

    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=[
            send_sms_code, register_user, login_user, get_user_profile,
            search_products, get_product_detail, get_categories,
            add_to_cart, get_cart, remove_from_cart,
            get_provinces, add_shipping_address, get_shipping_addresses,
            create_order, get_order_list, get_order_detail, cancel_order,
            get_payment_methods, initiate_payment, get_payment_status,
            apply_refund, get_refund_list, confirm_delivery
        ],
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
