# Google Play 南非区 - 审核注意事项与常见问题

## ⚠️ 审核政策红线

### 绝对禁止

| 违规类型 | 后果 | 说明 |
|---------|------|------|
| 虚假信息 | 永久封号 | 功能与描述严重不符 |
| 恶意软件 | 永久封号 | 包含恶意代码 |
| 儿童内容违规 | 永久封号 | 涉及未成年人保护问题 |
| 知识产权侵权 | 下架+警告 | 使用未授权商标/内容 |
| POPIA严重违规 | 下架+封号 | 非法收集用户数据 |

### 高风险行为

| 行为 | 风险 | 建议 |
|------|------|------|
| 诱导差评 | 警告+下架 | 禁止贿赂用户好评 |
| 隐藏功能 | 警告+下架 | 避免误导用户 |
| 竞争对手攻击 | 警告+下架 | 避免恶意比较 |
| 虚假评分 | 警告+删除 | 禁止刷评分 |

---

## 🔒 南非区特殊要求

### 1. POPIA数据保护法

**南非《个人信息保护法》(POPIA) 核心要求**：

#### 1.1 隐私政策必需内容

```markdown
隐私政策必须包含以下章节：

1. 数据控制者信息
   - 公司名称
   - 注册地址
   - 联系方式
   - 数据保护官(PO)信息

2. 个人信息收集
   - 收集的个人信息类型
   - 收集方式
   - 法律依据

3. 信息使用目的
   - 主要用途
   - 次要用途
   - 用户同意获取方式

4. 信息共享
   - 第三方类型
   - 跨境传输国家
   - 数据保护措施

5. 数据安全
   - 安全技术措施
   - 组织管理措施
   - 泄露通知机制

6. 用户权利
   - 访问权
   - 更正权
   - 删除权
   - 反对权
   - 便携权

7. 投诉机制
   - 内部申诉渠道
   - 监管机构联系方式
   - Information Regulator South Africa
```

#### 1.2 应用内隐私要求

```kotlin
// 敏感权限申请
private val permissionLauncher = registerForActivityResult(
    ActivityResultContracts.RequestMultiplePermissions()
) { permissions ->
    when {
        // 位置权限处理
        permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true -> {
            // 明确告知用途
            showLocationPurposeDialog()
        }
        // 短信权限处理
        permissions[Manifest.permission.READ_SMS] == true -> {
            // 仅用于OTP验证
            verifySMSPurpose()
        }
    }
}

// 首次启动隐私同意
class PrivacyConsentActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // 必需选项（不能默认同意）
        val privacyDialog = PrivacyDialogBuilder(this)
            .setTitle("Privacy & Data Protection")
            .addSection(
                title = "Information We Collect",
                items = listOf(
                    "Personal information (name, email, phone)",
                    "Address for delivery",
                    "Payment information",
                    "Location data (with consent)",
                    "Device information"
                )
            )
            .addSection(
                title = "How We Use Your Data",
                items = listOf(
                    "Process your orders",
                    "Improve our services",
                    "Send order updates"
                )
            )
            .setRequiredCheckbox(
                text = "I agree to the Privacy Policy and consent to data processing",
                isRequired = true  // 必选，不能默认勾选
            )
            .setOptionalCheckbox(
                text = "I consent to marketing communications",
                isDefaultChecked = false  // 可选，默认不勾选
            )
            .build()
        
        privacyDialog.show()
    }
}
```

### 2. 消费者保护法

**南非《消费者保护法》(CPA) 核心要求**：

#### 2.1 退款政策

```markdown
必须提供以下退款政策：

【退货期限】
- 实体商品：14天内可退货
- 数字商品：7天内可退款

【退货条件】
- 商品未使用/损坏
- 保留原始包装
- 附带购买凭证

【退款方式】
- 原支付渠道退款
- 退款周期：5-7个工作日

【例外情况】
- 定制商品不可退货
- 过期商品不可退货
- 已拆封的私密商品不可退货
```

#### 2.2 价格标识

```kotlin
// 价格显示规范
data class PriceDisplay(
    val amount: BigDecimal,
    val currency: Currency = Currency.ZAR,
    val showInclusiveVAT: Boolean = true,  // 必须显示含税价格
    val showOriginalPrice: Boolean? = null,  // 促销时显示原价
    val showSavings: Boolean? = null  // 促销时显示节省金额
)

// 正确示例
PriceDisplay(
    amount = 299.00.toBigDecimal(),
    currency = Currency.ZAR,
    showInclusiveVAT = true
)
// 显示: "R299.00 (VAT inclusive)"

// 促销示例
PriceDisplay(
    amount = 199.00.toBigDecimal(),
    currency = Currency.ZAR,
    showInclusiveVAT = true,
    showOriginalPrice = 299.00.toBigDecimal(),
    showSavings = 100.00.toBigDecimal()
)
// 显示: "R199.00 (Was R299.00, Save R100.00)"
```

### 3. 支付合规

#### 3.1 允许的支付方式

| 支付方式 | 集成商 | 说明 |
|---------|-------|------|
| Visa/Mastercard | PayStack | 南非主流 |
| Ozow | Ozow | 即时转账 |
| PayPal | PayPal | 国际用户 |
| 移动支付 | Peach Payments | 本地整合 |

#### 3.2 禁止的支付方式

| 支付方式 | 原因 |
|---------|------|
| 加密货币直接支付 | 无监管框架 |
| 现金快递(COD) | 高风险欺诈 |
| 第三方钱包 | 未授权 |

#### 3.3 支付SDK配置

```kotlin
// AndroidManifest.xml
<meta-data
    android:name="com.paystack.sdk.PublicKey"
    android:value="${PAYSTACK_PUBLIC_KEY}" />

<!-- 南非支付流程 -->
class PaymentActivity : AppCompatActivity() {
    
    private lateinit var paystack: Paystack
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // 显示所有费用明细
        showPriceBreakdown()
    }
    
    private fun showPriceBreakdown() {
        val totalAmount = calculateTotal()
        val shippingFee = calculateShipping()
        val customsDuty = calculateCustomsDuty()
        val vat = calculateVAT()
        
        priceBreakdownView.setItems(listOf(
            PriceItem("Subtotal", totalAmount),
            PriceItem("Shipping", shippingFee),
            PriceItem("Customs Duty", customsDuty),
            PriceItem("VAT (15%)", vat),
            PriceItem("Total", totalAmount + shippingFee + customsDuty + vat)
        ))
    }
}
```

---

## 🛡️ 审核常见问题

### 问题1：应用崩溃/无响应

**错误表现**：
```
Your app crashed during review.
Device: Pixel 7, Android 14
```

**解决方案**：
```bash
# 全面测试命令
./gradlew clean assembleRelease

# 使用Firebase Test Lab
gcloud firebase test android run \
  --type instrumentation \
  --app app/build/outputs/apk/release/app-release.apk \
  --device model=Pixel7,version=34,locale=za_EN
```

### 问题2：权限申请过多

**错误表现**：
```
Your app requests excessive permissions that are not required for core functionality.
```

**解决方案**：
```kotlin
// 只申请核心权限
private val corePermissions = arrayOf(
    Manifest.permission.INTERNET,
    Manifest.permission.ACCESS_NETWORK_STATE
)

// 可选权限（动态申请）
private val optionalPermissions = arrayOf(
    Manifest.permission.ACCESS_FINE_LOCATION,  // 仅用于自提点推荐
    Manifest.permission.CAMERA,  // 仅用于商品拍摄
    Manifest.permission.READ_SMS  // 仅用于OTP验证
)

// 使用前检查
if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) 
    != PackageManager.PERMISSION_GRANTED) {
    // 仅在真正需要时申请
    permissionLauncher.launch(arrayOf(Manifest.permission.ACCESS_FINE_LOCATION))
}
```

### 问题3：内容分级未完成

**错误表现**：
```
Your app content rating questionnaire is incomplete.
```

**解决方案**：
在Play Console完成问卷：
```
1. 暴力内容：无
2. 粗俗语言：无
3. 赌博内容：无
4. 恐怖内容：无
5. 毒品相关：无
6. 仇恨言论：无
7. 性暗示内容：无
8. 伤害内容：无
```

### 问题4：广告标识缺失

**错误表现**：
```
Your app contains ads but the Ads ID declaration is not completed.
```

**解决方案**：
在Play Console填写广告ID声明：
```
Is your app an ad-supported app? → Yes/No
Are you using advertising ID? → Yes/No
```

### 问题5：应用内购买未配置

**错误表现**：
```
Your app has in-app purchases but they are not configured.
```

**解决方案**：
```kotlin
// 明确区分免费功能和付费功能
class SubscriptionManager {
    
    // 免费功能
    fun browseProducts() { /* 所有人都能用 */ }
    fun addToCart() { /* 所有人都能用 */ }
    
    // 付费功能（Premium）
    fun unlockPremiumFeatures() {
        // 必须使用Google Play Billing
        val billingClient = BillingClient.newBuilder(this)
            .setListener(this)
            .enablePendingPurchases()
            .build()
    }
}
```

### 问题6：隐私政策URL无效

**错误表现**：
```
Your privacy policy URL is invalid or the page does not contain a privacy policy.
```

**解决方案**：
```markdown
隐私政策页面要求：
1. 使用HTTPS
2. 页面标题包含"Privacy Policy"
3. 包含公司联系信息
4. 可被搜索引擎收录
5. 包含POPIA合规说明
```

---

## ⏱️ 审核时间线

### 首次提交

| 阶段 | 时间 | 说明 |
|------|------|------|
| 提交审核 | Day 0 | 提交到Play Console |
| 初步审核 | Day 1-3 | 格式和基本合规检查 |
| 功能测试 | Day 2-5 | 自动化测试+人工测试 |
| 安全扫描 | Day 3-6 | 恶意软件扫描 |
| 最终审核 | Day 5-7 | 政策合规确认 |
| 发布 | Day 7 | 通过后自动发布 |

### 更新审核

| 更新类型 | 审核时间 |
|---------|---------|
| 紧急审核（付费） | 1天 |
| 小幅更新 | 1-3天 |
| 大版本更新 | 3-7天 |

### 加速审核

**申请条件**：
- 安全漏洞修复
- 关键Bug修复
- 法规合规更新

**申请方式**：
1. Play Console → Help → Contact Us
2. 选择"Request expedited review"
3. 说明紧急原因

---

## 📧 审核申诉

### 申诉流程

1. **查看拒绝原因**
   - Play Console → Policy Status
   - 详细阅读违规说明

2. **准备申诉材料**
   - 修复证明
   - 代码变更说明
   - 测试截图

3. **提交申诉**
   ```markdown
   Subject: Appeal for App Rejection - [Package Name]
   
   Dear Google Play Review Team,
   
   We have addressed the following issues:
   
   1. [Issue Description]
      - Root Cause: [原因]
      - Fix Applied: [修复措施]
      - Verification: [验证截图]
   
   2. [Additional Information]
      [补充说明]
   
   We kindly request a re-review of our application.
   
   Best regards,
   [Developer Name]
   ```

4. **等待回复**
   - 通常3-5个工作日
   - 可通过邮件追踪进度

---

## 🧪 自检清单

### 上架前必检

```markdown
【应用功能】
- [ ] 应用可正常启动
- [ ] 所有功能与描述一致
- [ ] 无崩溃/ANR问题
- [ ] 权限申请合理

【隐私合规】
- [ ] 隐私政策已发布
- [ ] POPIA合规声明已添加
- [ ] 用户数据收集已最小化
- [ ] 敏感权限有明确用途

【支付合规】
- [ ] 使用授权支付SDK
- [ ] 价格包含税费说明
- [ ] 退款政策明确

【内容规范】
- [ ] 无虚假宣传
- [ ] 无侵权内容
- [ ] 无敏感政治内容
- [ ] 截图无不当内容

【素材规范】
- [ ] 图标尺寸正确
- [ ] 截图尺寸正确
- [ ] 描述无超字符
- [ ] 隐私政策URL有效
```

---

## 📞 支持渠道

| 渠道 | 链接 | 用途 |
|------|------|------|
| Play Console帮助 | https://support.google.com/googleplay/android-developer | 政策解答 |
| 开发者社区 | https://community.google.com/ | 经验分享 |
| 紧急申诉 | Play Console → Help → Contact Us | 紧急问题 |
| 政策状态 | Play Console → Policy Status | 查看违规详情 |

---

## 📝 南非特有检查项

```markdown
【南非本地化】
- [ ] 价格显示为ZAR
- [ ] 南非省份数据完整
- [ ] 支持南非手机号注册
- [ ] 支持南非邮编格式
- [ ] 物流覆盖南非全境

【南非支付】
- [ ] Ozow支付集成
- [ ] PayStack支付集成
- [ ] 无禁止的支付方式

【南非语言】
- [ ] 至少支持英语
- [ ] 推荐支持南非荷兰语
- [ ] 祖鲁语界面可选

【南非节日】
- [ ] 考虑南非节日促销
- [ ] 避开敏感日期发布
```

---

*最后更新：2024*
