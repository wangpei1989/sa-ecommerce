package com.sacomerce.app

import android.app.Application
import com.sacomerce.app.config.SAConfig
import com.sacomerce.app.network.ApiClient
import com.sacomerce.app.storage.SecureStorage
import com.sacomerce.app.analytics.Analytics

/**
 * SA Commerce Application
 * 南非跨境电商APP主应用类
 */
class SACommerceApp : Application() {

    override fun onCreate() {
        super.onCreate()
        instance = this
        
        // 初始化南非配置
        initSAConfig()
        
        // 初始化网络
        initNetwork()
        
        // 初始化安全存储
        initSecureStorage()
        
        // 初始化分析
        initAnalytics()
    }

    private fun initSAConfig() {
        // 南非区域配置
        SAConfig.initialize(this)
        
        // 设置默认货币
        SAConfig.defaultCurrency = "ZAR"
        SAConfig.defaultLocale = "en"
        SAConfig.taxRate = 0.15  // 15% VAT
        SAConfig.supportedProvinces = listOf(
            "Gauteng", "Western Cape", "KwaZulu-Natal",
            "Eastern Cape", "Free State", "Limpopo",
            "Mpumalanga", "North West", "Northern Cape"
        )
    }

    private fun initNetwork() {
        // 初始化API客户端
        ApiClient.initialize(
            baseUrl = SAConfig.apiBaseUrl,
            timeout = 30_000L,
            enableLogging = !SAConfig.isRelease
        )
    }

    private fun initSecureStorage() {
        // 初始化安全存储（POPIA合规）
        SecureStorage.initialize(this)
    }

    private fun initAnalytics() {
        // 初始化分析
        Analytics.initialize(this)
    }

    companion object {
        lateinit var instance: SACommerceApp
            private set
    }
}
