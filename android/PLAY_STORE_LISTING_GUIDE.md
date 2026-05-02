# Google Play 南非区上架完整流程指南

## 📋 目录
1. [上架前准备](#1-上架前准备)
2. [开发者账号注册](#2-开发者账号注册)
3. [应用创建与配置](#3-应用创建与配置)
4. [素材准备清单](#4-素材准备清单)
5. [应用审核提交](#5-应用审核提交)
6. [审核标准与注意事项](#6-审核标准与注意事项)
7. [上线后维护](#7-上线后维护)

---

## 1. 上架前准备

### 1.1 资质准备

| 资质类型 | 说明 | 办理周期 |
|---------|------|---------|
| 营业执照 | 南非公司注册证书或海外公司公证文件 | 2-4周 |
| 税务登记 | SARS增值税注册证书（如需） | 1-2周 |
| 银行账户 | 南非本地银行账户或国际支付账户 | 2-3周 |
| 隐私政策 | 符合POPIA法案的隐私政策 | 1周 |
| 退款政策 | 明确的14天退款政策 | - |

### 1.2 开发者账号类型

| 类型 | 价格 | 功能 | 适用场景 |
|------|------|------|---------|
| 个人开发者 | $25一次性 | 单账号无限应用 | 个人/小团队 |
| 公司开发者 | $25一次性 | 多账号、团队协作 | 企业用户 |

### 1.3 技术准备

```bash
# 构建命令
./gradlew assembleRelease          # 标准发布版
./gradlew assembleZaRelease         # 南非优化版
./gradlew assembleMtnRelease        # MTN定制版
./gradlew assembleVodacomRelease    # Vodacom定制版

# 签名配置
# 确保 release-keystore.jks 已安全存储
# 记录以下信息用于Play Console配置：
# - Key alias
# - Keystore password
# - Key password
```

---

## 2. 开发者账号注册

### 2.1 注册流程

1. **访问Play Console**
   ```
   https://play.google.com/console
   ```

2. **创建账号**
   - 点击"注册"
   - 选择账号类型（个人/公司）
   - 填写开发者名称（将显示在应用商店）

3. **完成付款**
   - 支付$25注册费
   - 接受开发者分发协议

4. **验证身份**
   - 上传身份证件
   - 公司账号需提供注册文件

### 2.2 南非区特殊要求

- 开发者地址需填写真实地址（用于税务）
- 如使用海外公司，需提供南非代理人信息
- POPIA合规负责人联系方式

---

## 3. 应用创建与配置

### 3.1 创建应用

1. 登录 Play Console
2. 点击"创建应用"
3. 填写基本信息：

| 字段 | 说明 | 示例 |
|------|------|------|
| 应用名称 | 商店显示名称 | SA Commerce |
| 应用语言 | 默认语言 | English (en) |
| 应用类型 | 移动应用/游戏 | 移动应用 |
| 免费/付费 | 商业模式 | 免费（含应用内购买） |

### 3.2 应用配置

#### 3.2.1 商店信息

**应用名称**：`SA Commerce - 南非跨境购物`

**简短说明**（80字符内）：
```
Shop from China & global brands with fast delivery to South Africa.
```

**完整说明**（4000字符内）：
```
【About SA Commerce】

SA Commerce is your trusted cross-border shopping platform connecting South Africa with global markets.

✨ Key Features
• Browse millions of products from verified international sellers
• Multiple payment options: Credit Card, EFT, Ozow, PayPal
• Real-time logistics tracking from China to your door
• Local pickup points across South Africa
• Secure customs clearance support

🛍️ Why Choose Us
• Competitive prices with ZAR currency
• Multi-language support (English, Afrikaans, Zulu, etc.)
• 14-day easy returns
• 24/7 customer support
• POPIA compliant data protection

📦 Shipping
• Standard: 7-14 business days
• Express: 5-7 business days
• Real-time tracking available

💳 Payment Methods
• Visa / Mastercard
• Ozow Instant EFT
• PayPal
• Cash on Delivery (select areas)

📞 Contact Us
Email: support@sacomerce.co.za
Phone: 0860 100 200

【关于我们】

SA Commerce是您值得信赖的跨境购物平台，连接南非与全球市场。

• 来自中国的优质商品
• 安全便捷的支付方式
• 实时物流追踪
• 南非全境自提点
```

#### 3.2.2 商品详情

**应用图标**：
- 尺寸：512×512 PNG
- 要求：纯色背景、无阴影、支持自适应图标

**截图**：
- 手机截图：1080×1920 PNG（最少2张，最多8张）
- 7英寸平板：1200×1920 PNG
- 10英寸平板：1920×1200 PNG
- 内容：展示核心功能流程

**Feature Graphic**（可选）：
- 尺寸：1024×500 PNG
- 用途：Play Store首页展示

---

## 4. 素材准备清单

### 4.1 必需素材

| 素材类型 | 规格 | 文件格式 | 数量 |
|---------|------|---------|------|
| 应用图标 | 512×512px | PNG | 1 |
| 应用截图(手机) | 1080×1920px | PNG/JPG | 2-8 |
| 截图(7寸平板) | 1200×1920px | PNG/JPG | 0-8 |
| 截图(10寸平板) | 1920×1200px | PNG/JPG | 0-8 |
| Short Description | 80字符 | 文本 | 1 |
| Full Description | 4000字符 | 文本 | 1 |

### 4.2 Feature Graphic模板

```
┌─────────────────────────────────────────────┐
│                                             │
│   [应用图标 48×48]                           │
│                                             │
│   应用名称 (醒目)                            │
│   简短卖点 (副标题)                          │
│                                             │
│   [CTA按钮或商品图片]                        │
│                                             │
│   背景色: 品牌主色调或渐变                    │
│                                             │
└─────────────────────────────────────────────┘
```

### 4.3 应用截图设计建议

**必包含内容**：
1. 首页/商品浏览页
2. 商品详情页
3. 购物车页面
4. 支付页面
5. 订单追踪页面

**设计规范**：
- 使用真实南非本地商品数据
- 展示ZAR货币价格
- 显示南非城市配送场景
- 多语言切换功能展示

### 4.4 商店图标规范

| 元素 | 要求 |
|------|------|
| 尺寸 | 512×512px |
| 安全区域 | 中心 384×384px 内不放重要内容 |
| 圆角 | 系统自动生成 |
| 背景 | 纯色或简单渐变 |
| 文字 | 避免在图标中放置文字 |
| 格式 | 32-bit PNG |

---

## 5. 应用审核提交

### 5.1 内容分级

**年龄分级问卷**：
- 暴力内容：无
- 粗俗语言：无
- 赌博内容：无
- 恐怖内容：无
- 毒品相关：无

**内容标签**：在线购买实体商品

### 5.2 上架地区选择

**南非区上架配置**：
```
上架地区：South Africa (ZA)
默认分发：是
价格：免费
年龄限制：3+
内容分级：所有用户
```

### 5.3 商品详情页配置

**目标用户**：
- 主要：18-45岁
- 次要：商务人士、跨境购物爱好者

**类别选择**：
- 主类别：Shopping
- 子类别：Shopping
- 标签：ecommerce, cross-border, south africa

### 5.4 提交检查清单

- [ ] 应用图标已上传
- [ ] 至少2张手机截图
- [ ] Short Description已填写
- [ ] Full Description已填写
- [ ] 应用图标符合规范
- [ ] 截图不包含敏感信息
- [ ] 价格和分发设置正确
- [ ] 内容分级已完成
- [ ] 隐私政策URL已填写
- [ ] 广告标识已完成

---

## 6. 审核标准与注意事项

### 6.1 常见拒绝原因及解决方案

| 拒绝原因 | 说明 | 解决方案 |
|---------|------|---------|
| 崩溃/无响应 | 应用无法正常启动 | 全面测试、修复ANR |
| 权限滥用 | 申请不必要权限 | 仅申请必要权限 |
| 支付政策违规 | 支付流程不合规 | 使用官方支付SDK |
| 虚假信息 | 功能描述不实 | 准确描述功能 |
| 版权侵权 | 使用未授权内容 | 使用原创素材 |
| POPIA违规 | 隐私数据处理不当 | 合规隐私政策 |

### 6.2 南非区特殊审核要求

#### 6.2.1 POPIA合规（关键）

**必须包含**：
- 明确的隐私政策
- 用户数据收集说明
- 数据存储期限说明
- 用户删除账户功能
- 第三方共享说明

**隐私政策必须包含**：
```
1. 信息收集
   - 个人信息类型
   - 收集方式
   - 收集目的

2. 信息使用
   - 如何使用您的信息
   - 法律依据

3. 信息共享
   - 第三方类型
   - 跨境传输说明

4. 信息安全
   - 安全措施
   - 数据加密

5. 用户权利
   - 访问权
   - 更正权
   - 删除权
   - 投诉权

6. 联系信息
   - 隐私官联系方式
   - 投诉渠道
```

#### 6.2.2 消费者保护

- 退款政策必须明确
- 商品信息必须准确
- 配送时间必须合理
- 联系方式必须有效

### 6.3 支付合规要求

**允许的支付方式**：
- 信用卡/借记卡（通过PayStack等授权机构）
- Ozow即时转账
- PayPal
- 南非本地电子支付

**禁止的支付方式**：
- 加密货币直接支付
- 现金快递(Cash on Delivery需谨慎)
- 未授权的第三方支付

### 6.4 审核时间

| 阶段 | 预计时间 |
|------|---------|
| 首次审核 | 3-7天 |
| 更新审核 | 1-3天 |
| 紧急审核（付费） | 1天 |

---

## 7. 上线后维护

### 7.1 监控指标

| 指标 | 目标值 |
|------|-------|
| 崩溃率 | < 0.5% |
| ANR率 | < 0.1% |
| 评分 | ≥ 4.0星 |
| 安装量 | 持续增长 |
| 卸载率 | < 20% |

### 7.2 用户反馈处理

- 48小时内回复用户评价
- 优先处理1-2星评价
- 收集用户建议迭代产品

### 7.3 版本更新流程

1. 准备更新内容
2. 更新Version Code/Name
3. 提交审核
4. 审核通过后自动发布

### 7.4 紧急情况处理

**应用被下架**：
1. 查收Play Console通知
2. 了解违规原因
3. 修复问题
4. 提交申诉

**被恶意差评**：
1. 收集证据
2. 联系Google支持
3. 引导用户正确评价

---

## 📞 支持资源

- Google Play Console帮助：https://support.google.com/googleplay/android-developer
- 开发者社区：https://community.google.com/
- 南非POPIA指南：https://popia.co.za/

---

*最后更新：2024*
