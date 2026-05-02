# Google Play 南非区 - 素材清单与设计规范

## 📁 素材文件结构

```
android/
├── assets/
│   └── store/
│       ├── icons/
│       │   ├── app_icon_512.png          # 应用图标512px
│       │   └── adaptive_icon_legacy.png   # 自适应图标
│       ├── screenshots/
│       │   ├── phone/
│       │   │   ├── screenshot_01_home.png
│       │   │   ├── screenshot_02_search.png
│       │   │   ├── screenshot_03_product.png
│       │   │   ├── screenshot_04_cart.png
│       │   │   ├── screenshot_05_payment.png
│       │   │   ├── screenshot_06_tracking.png
│       │   │   ├── screenshot_07_profile.png
│       │   │   └── screenshot_08_pickup.png
│       │   ├── tablet_7inch/
│       │   │   ├── screenshot_tab7_01.png
│       │   │   └── screenshot_tab7_02.png
│       │   └── tablet_10inch/
│       │       ├── screenshot_tab10_01.png
│       │       └── screenshot_tab10_02.png
│       ├── feature_graphic/
│       │   ├── feature_graphic_1024x500.png
│       │   └── tv_banner_1920x720.png
│       └── promo_video/
│           └── promo_video_30s.mp4
├── strings/
│   ├── values/strings.xml                 # 英语
│   ├── values-af/strings.xml              # 南非荷兰语
│   ├── values-zu/strings.xml              # 祖鲁语
│   ├── values-xh/strings.xml              # 科萨语
│   ├── values-nso/strings.xml             # 北索托语
│   └── values-tn/strings.xml              # 茨瓦纳语
└── PLAY_STORE_LISTING_GUIDE.md
```

---

## 🎨 应用图标规范

### 1. Play Store图标

| 属性 | 规格 |
|------|------|
| 尺寸 | 512×512px |
| 文件格式 | PNG (32-bit) |
| 命名 | app_icon_512.png |
| 背景 | 纯色 (#E53935 品牌红) |
| 安全区 | 中心 384×384px |

### 2. 自适应图标

| 属性 | 规格 |
|------|------|
| 前景 | 512×512px PNG (透明背景) |
| 背景 | 512×512px PNG (纯色) |
| 遮罩 | XML adaptive-icon 定义 |

### 3. 图标设计指南

```
✅ 正确做法：
- 使用简洁的图形
- 高对比度配色
- 品牌识别度高
- 任意尺寸清晰可辨

❌ 错误做法：
- 使用照片作为图标
- 包含过多细节
- 使用渐变过于复杂
- 文字超过3个字符
```

---

## 📱 应用截图规范

### 1. 手机截图

| 属性 | 规格 |
|------|------|
| 最小尺寸 | 1080×1920px |
| 推荐尺寸 | 1080×1920px 或更高 |
| 宽高比 | 9:16 |
| 文件格式 | PNG 或 24-bit JPG |
| 状态栏 | 必须包含 |
| 导航栏 | 必须包含 |

### 2. 平板截图

| 类型 | 最小尺寸 | 推荐尺寸 |
|------|---------|---------|
| 7英寸 | 1200×1920px | 1200×1920px |
| 10英寸 | 1920×1200px | 1920×1200px |
| TV | 1920×720px | 1920×720px |

### 3. 截图命名规范

```
格式：screenshot_{device}_{sequence}.{ext}

示例：
- screenshot_phone_01.png
- screenshot_phone_02.png
- screenshot_tab7_01.png
- screenshot_tab10_01.png
```

---

## 🖼️ Feature Graphic

### 1. 标准Feature Graphic

| 属性 | 规格 |
|------|------|
| 尺寸 | 1024×500px |
| 文件格式 | JPG 或 PNG |
| 文件大小 | < 150KB |
| 命名 | feature_graphic_1024x500.png |

### 2. TV Banner

| 属性 | 规格 |
|------|------|
| 尺寸 | 1920×720px |
| 文件格式 | JPG 或 PNG |
| 命名 | tv_banner_1920x720.png |

### 3. Feature Graphic 设计模板

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  ┌──────┐                                                    │
│  │ LOGO │  品牌名                                             │
│  └──────┘  简短标语（12字以内）                               │
│                                                              │
│                                                              │
│                        [主视觉图]                            │
│                                                              │
│                                                              │
│  行动号召按钮                                                 │
│                                                              │
│  背景色渐变：从 #E53935 到 #FF7043                           │
└──────────────────────────────────────────────────────────────┘
```

---

## 📹 宣传视频（可选）

| 属性 | 规格 |
|------|------|
| 时长 | 30秒（推荐）或 15秒 |
| 分辨率 | 1080×1920px (竖屏) |
| 格式 | MP4 (H.264) |
| 文件大小 | < 100MB |
| 宽高比 | 9:16 |

---

## ✍️ 文案规范

### 1. 标题规范

| 字段 | 最大字符 | 当前内容 |
|------|---------|---------|
| 应用名称 | 30字符 | SA Commerce |
| 短标题 | 30字符 | SA Commerce |

### 2. 描述文案

| 字段 | 最大字符 | 说明 |
|------|---------|------|
| 短描述 | 80字符 | 首页展示，需吸引用户 |
| 完整描述 | 4000字符 | 详细介绍功能和优势 |

### 3. 文案示例

**短描述（80字符）**：
```
Shop global brands with fast delivery to South Africa. Multiple payments accepted.
```

**完整描述模板**：
```markdown
[应用名称] is South Africa's leading cross-border e-commerce platform.

【Key Features】
• Shop from China & global brands
• Multiple payment options
• Real-time tracking
• Local pickup points
• Multi-language support

【Why Choose Us】
• Best prices in ZAR
• Secure payments
• 14-day returns
• 24/7 support

【Shipping】
• Standard: 7-14 days
• Express: 5-7 days

【Contact】
support@sacomerce.co.za
```

---

## 🌐 多语言翻译要求

### 南非官方语言

| 语言 | ISO代码 | 应用内 | Play Store |
|------|---------|-------|------------|
| 英语 | en | ✅ | ✅ |
| 南非荷兰语 | af | ✅ | ✅ |
| 祖鲁语 | zu | ✅ | ✅ |
| 科萨语 | xh | ✅ | ✅ |
| 北索托语 | nso | ✅ | - |
| 茨瓦纳语 | tn | ✅ | - |
| 索托语 | st | ✅ | - |
| 聪加语 | ts | ✅ | - |
| 斯威士语 | ss | ✅ | - |
| 文达语 | ve | ✅ | - |
| 南非手语 | ssf | - | - |

### 翻译优先级

1. **必需翻译** (Play Store必需)
   - 应用名称
   - 短描述
   - 完整描述

2. **推荐翻译** (用户体验优化)
   - 应用图标文字
   - 主要功能界面
   - 错误提示

3. **可选翻译** (市场覆盖)
   - 全部界面
   - 推送通知
   - 帮助文档

---

## 🎯 截图内容建议

### 手机截图（8张）

| 序号 | 页面 | 内容建议 |
|------|------|---------|
| 1 | 首页 | 展示促销活动、南非本地化内容 |
| 2 | 搜索 | 显示商品搜索结果、筛选功能 |
| 3 | 商品详情 | 展示商品图片、价格(ZAR)、配送信息 |
| 4 | 购物车 | 显示已选商品、优惠券入口 |
| 5 | 支付 | 展示多种支付方式（Ozow、Card等） |
| 6 | 物流追踪 | 显示包裹实时位置 |
| 7 | 个人中心 | 订单、地址管理 |
| 8 | 自提点 | 展示南非地图、自提点列表 |

### 截图设计规范

```markdown
✅ 推荐内容：
- 南非本地商品
- ZAR货币价格展示
- 南非城市背景
- MTN/Vodacom运营商优惠
- 祖鲁语/南非荷兰语界面

❌ 避免内容：
- 外国地址信息
- 美元/欧元价格
- 与南非无关的商品
- 敏感政治内容
```

---

## 📋 素材检查清单

### 发布前必查

- [ ] 应用图标 512×512px PNG 已上传
- [ ] 自适应图标已配置
- [ ] 手机截图至少2张
- [ ] 所有截图尺寸正确
- [ ] Short Description < 80字符
- [ ] Full Description < 4000字符
- [ ] Feature Graphic 已上传
- [ ] 所有文本无拼写错误
- [ ] 图片无拉伸/变形
- [ ] 隐私政策URL已填写
- [ ] 南非区已选择分发

---

## 🔧 自动化生成脚本

```bash
#!/bin/bash
# 生成所需尺寸截图

# 源文件
SRC="source_screenshot.png"

# 生成各种尺寸
# 手机截图
convert $SRC -resize 1080x1920! screenshot_phone_01.png

# 7寸平板
convert $SRC -resize 1200x1920! screenshot_tab7_01.png

# 10寸平板
convert $SRC -resize 1920x1200! screenshot_tab10_01.png

# Feature Graphic
convert $SRC -resize 1024x500! feature_graphic.png

echo "All screenshots generated!"
```

---

## 📞 素材提交支持

如需设计帮助：
- Figma模板：https://figma.com/@sacomerce
- 设计规范：https://design.sacomerce.co.za
- 素材审核：assets@sacomerce.co.za

---

*最后更新：2024*
