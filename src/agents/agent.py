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
    from tools.sa_localization import (
        convert_to_zar, convert_from_zar, get_exchange_rates,
        get_supported_languages, translate, format_currency_zar,
        get_provinces as get_provinces_data, get_cities_by_province,
        validate_sa_phone, validate_sa_postal_code, validate_sa_address,
        check_network_status, get_offline_cache_policy,
        estimate_delivery_time as sa_estimate_delivery, calculate_shipping_fee
    )
    from tools.logistics_customs import (
        track_shipment, verify_tracking_number,
        find_pickup_points, get_pickup_point_detail,
        calculate_shipping_cost,
        get_customs_clearance_info, calculate_customs_duty,
        get_prohibited_items, estimate_total_delivery_time
    )
    from tools.merchant_tools import (
        register_merchant, get_merchant_profile, update_merchant_info, get_merchant_status,
        list_product, update_product, get_merchant_products, update_stock, get_product_categories,
        get_merchant_orders, get_order_detail, process_order, batch_process_orders,
        get_after_sales_list, process_after_sales, get_after_sales_detail, get_after_sales_stats,
        get_settlement_summary, get_transaction_details, request_withdrawal, get_withdrawal_history,
        get_merchant_balance, create_merchant_order, create_after_sales_ticket
    )

    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=[
            send_sms_code, register_user, login_user, get_user_profile,
            search_products, get_product_detail, get_categories,
            add_to_cart, get_cart, remove_from_cart,
            get_provinces_data, get_cities_by_province,
            add_shipping_address, get_shipping_addresses,
            create_order, get_order_list, get_order_detail, cancel_order,
            get_payment_methods, initiate_payment, get_payment_status,
            apply_refund, get_refund_list, confirm_delivery,
            # 本地化工具
            convert_to_zar, convert_from_zar, get_exchange_rates,
            get_supported_languages, translate, format_currency_zar,
            validate_sa_phone, validate_sa_postal_code, validate_sa_address,
            check_network_status, get_offline_cache_policy,
            sa_estimate_delivery, calculate_shipping_fee,
            # 物流与清关工具
            track_shipment, verify_tracking_number,
            find_pickup_points, get_pickup_point_detail,
            calculate_shipping_cost,
            get_customs_clearance_info, calculate_customs_duty,
            get_prohibited_items, estimate_total_delivery_time,
            # 商家端工具
            register_merchant, get_merchant_profile, update_merchant_info, get_merchant_status,
            list_product, update_product, get_merchant_products, update_stock, get_product_categories,
            get_merchant_orders, get_order_detail, process_order, batch_process_orders,
            get_after_sales_list, process_after_sales, get_after_sales_detail, get_after_sales_stats,
            get_settlement_summary, get_transaction_details, request_withdrawal, get_withdrawal_history,
            get_merchant_balance
        ],
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
