package com.sacomerce.app.config

import android.content.Context
import android.content.res.Configuration
import java.util.Locale

/**
 * 南非区域配置
 */
object SAConfig {
    
    lateinit var context: Context
        private set
    
    // API配置
    var apiBaseUrl: String = ""
        private set
    
    // 环境配置
    var isRelease: Boolean = false
        private set
    
    // 货币配置
    var defaultCurrency: String = "ZAR"
    var currencySymbol: String = "R"
    var taxRate: Double = 0.15  // 15% VAT
    
    // 语言配置
    var defaultLocale: String = "en"
    var supportedLocales: List<String> = listOf(
        "en", "af", "zu", "xh", "nso", "st", "tn"
    )
    
    // 省份配置
    var supportedProvinces: List<String> = emptyList()
    
    // 运营商配置
    var carrier: String = "GENERIC"
    
    // POPIA配置
    var dataRetentionDays: Int = 365
    var requireExplicitConsent: Boolean = true
    
    fun initialize(ctx: Context) {
        context = ctx.applicationContext
        
        // 根据构建类型设置API URL
        apiBaseUrl = if (isDebugBuild()) {
            "https://api-staging.sacomerce.co.za"
        } else {
            "https://api.sacomerce.co.za"
        }
    }
    
    private fun isDebugBuild(): Boolean {
        return context.applicationInfo?.flags?.and(
            android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE
        ) != 0
    }
    
    /**
     * 南非手机号验证
     */
    fun validatePhone(phone: String): Boolean {
        // 南非手机号格式：+27XXXXXXXXX 或 0XXXXXXXXX
        val regex = Regex("^(\\+27|0)[6-8][1-9]\\d{7}$")
        return regex.matches(phone)
    }
    
    /**
     * 南非邮编验证
     */
    fun validatePostalCode(code: String): Boolean {
        // 南非邮编：4位数字
        val regex = Regex("^\\d{4}$")
        return regex.matches(code)
    }
    
    /**
     * 格式化ZAR货币
     */
    fun formatCurrency(amount: Double): String {
        return "$currencySymbol%.2f".format(amount)
    }
    
    /**
     * 设置应用语言
     */
    fun setAppLocale(localeCode: String) {
        val locale = Locale(localeCode)
        Locale.setDefault(locale)
        
        val config = Configuration(context.resources.configuration)
        config.setLocale(locale)
        
        context.createConfigurationContext(config)
    }
    
    /**
     * 南非省份数据
     */
    object Provinces {
        val GAUTENG = Province("GP", "Gauteng", listOf("Johannesburg", "Pretoria", "Soweto"))
        val WESTERN_CAPE = Province("WC", "Western Cape", listOf("Cape Town", "Stellenbosch", "Paarl"))
        val KWAZULU_NATAL = Province("KZN", "KwaZulu-Natal", listOf("Durban", "Pietermaritzburg", "Richards Bay"))
        val EASTERN_CAPE = Province("EC", "Eastern Cape", listOf("Port Elizabeth", "East London", "Makhanda"))
        val FREE_STATE = Province("FS", "Free State", listOf("Bloemfontein", "Welkom", "Bethlehem"))
        val LIMPOPO = Province("LP", "Limpopo", listOf("Polokwane", "Thabazimbi", "Mokopane"))
        val MPUMALANGA = Province("MP", "Mpumalanga", listOf("Nelspruit", "Witbank", "Middleburg"))
        val NORTH_WEST = Province("NW", "North West", listOf("Rustenburg", "Klerksdorp", "Potchefstroom"))
        val NORTHERN_CAPE = Province("NC", "Northern Cape", listOf("Kimberley", "Upington", "Springbok"))
        
        val all = listOf(
            GAUTENG, WESTERN_CAPE, KWAZULU_NATAL, EASTERN_CAPE,
            FREE_STATE, LIMPOPO, MPUMALANGA, NORTH_WEST, NORTHERN_CAPE
        )
        
        fun findByCode(code: String): Province? = all.find { it.code == code }
        fun findByName(name: String): Province? = all.find { 
            it.name.equals(name, ignoreCase = true) 
        }
    }
    
    data class Province(
        val code: String,
        val name: String,
        val cities: List<String>
    )
    
    /**
     * 支付方式配置
     */
    object PaymentMethods {
        val PAYSTACK = PaymentMethod("paystack", "Credit/Debit Card", true)
        val OZOW = PaymentMethod("ozow", "Ozow Instant EFT", true)
        val PAYPAL = PaymentMethod("paypal", "PayPal", true)
        val CARD = PaymentMethod("card", "Card Payment", true)
        
        val all = listOf(PAYSTACK, OZOW, PAYPAL, CARD)
    }
    
    data class PaymentMethod(
        val code: String,
        val displayName: String,
        val enabled: Boolean
    )
    
    /**
     * 物流配置
     */
    object Logistics {
        val FREE_SHIPPING_THRESHOLD = 500.0  // R500以上免运费
        val STANDARD_DELIVERY_DAYS = mapOf(
            "GP" to 1..2,
            "WC" to 2..3,
            "KZN" to 2..3,
            "EC" to 3..4,
            "FS" to 3..4,
            "LP" to 4..5,
            "MP" to 3..4,
            "NW" to 4..5,
            "NC" to 5..7
        )
        
        val SHIPPING_RATES = mapOf(
            "GP" to 0.0,
            "WC" to 45.0,
            "KZN" to 55.0,
            "EC" to 65.0,
            "FS" to 65.0,
            "LP" to 75.0,
            "MP" to 65.0,
            "NW" to 75.0,
            "NC" to 85.0
        )
        
        val REMOTE_AREA_SUPPLEMENT = 30.0  // 偏远地区附加费
    }
}
