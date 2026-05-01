# 🇿🇦 South Africa E-commerce Agent

南非跨境电商智能助手，基于 Coze 平台构建。

## 功能模块

### 1. 商品管理
- 商品搜索
- 商品详情查询
- 商品分类浏览

### 2. 订单管理
- 创建订单
- 查询订单状态
- 取消订单
- 查看订单列表

### 3. 物流配送
- 物流追踪
- 自提点查询
- 运费计算

### 4. 南非本地化
- 南非兰特 (ZAR) 货币支持
- 多语言支持 (英语、祖鲁语、阿非利堪斯语等)
- 南非手机号验证
- 南非邮编验证
- 南非省份数据

### 5. 支付方式
- 信用卡/借记卡
- Instant EFT
- Ozow 即时支付
- PayPal

### 6. 用户中心
- 用户信息管理
- 收货地址管理

### 7. 营销功能
- 促销活动
- 优惠券领取与使用
- 积分系统

## 项目结构

```
src/
├── agents/
│   └── agent.py          # Agent 核心入口
├── tools/
│   ├── product_tool.py    # 商品工具
│   ├── order_tool.py      # 订单工具
│   ├── shipping_tool.py   # 物流工具
│   ├── payment_tool.py    # 支付工具
│   ├── user_tool.py      # 用户工具
│   ├── promotion_tool.py  # 营销工具
│   └── zar_currency.py   # 本地化工具
└── storage/
    └── memory/
        └── memory_saver.py # 记忆管理
```

## 快速开始

### 1. 安装依赖
```bash
uv sync
```

### 2. 配置模型
编辑 `config/agent_llm_config.json`，配置您的模型参数。

### 3. 启动服务
```bash
python src/main.py
```

### 4. 运行测试
```bash
pytest tests/
```

## 南非电商政策说明

- **运费规则**: 订单金额超过 R500 享受免费配送
- **退货政策**: 收货后 30 天内可申请退货
- **支付方式**: 不支持货到付款 (跨境限制)
- **配送范围**: 仅支持南非境内配送

## 货币说明

- 所有金额以 **分 (cent)** 为单位存储
- 前端显示需除以 100 转为兰特
- 示例: `29900` 分 = `R299.00`
