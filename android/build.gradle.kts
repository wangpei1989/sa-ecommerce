// 南非跨境电商APP - 根项目构建配置
plugins {
    id 'com.android.application' version '8.2.0' apply false
    id 'org.jetbrains.kotlin.android' version '1.9.21' apply false
    id 'com.google.gms.google-services' version '4.4.0' apply false
    id 'org.jetbrains.kotlin.plugin.serialization' version '1.9.21' apply false
}

// 南非区版本号配置
ext {
    // 版本配置
    VERSION_MAJOR = 1
    VERSION_MINOR = 0
    VERSION_PATCH = 0
    VERSION_NAME = "${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}"
    VERSION_CODE = 1
    
    // 南非特定配置
    COUNTRY_CODE = "ZA"
    DEFAULT_CURRENCY = "ZAR"
    DEFAULT_LANGUAGE = "en"
    
    // SDK版本
    MIN_SDK = 24
    TARGET_SDK = 34
    COMPILE_SDK = 34
    
    // 构建配置
    IS_SA_BUILD = true
}

// 南非区域属性
allprojects {
    ext {
        saConfig = [
            country: "South Africa",
            currency: "ZAR",
            currencySymbol: "R",
            taxRate: 0.15,  // 15% VAT
            supportedLanguages: ["en", "af", "zu", "xh", "nso", "st", "tn"],
            provinces: [
                "Gauteng", "Western Cape", "KwaZulu-Natal",
                "Eastern Cape", "Free State", "Limpopo",
                "Mpumalanga", "North West", "Northern Cape"
            ],
            pickupCarriers: ["Pudo", "Paxie", "South African Post Office", "Boxer"],
            paymentMethods: ["PayStack", "Ozow", "PayPal", "Card"]
        ]
    }
}

// 南非特定仓库配置
 repositories {
    maven {
        url "https://maven.sacomerce.co.za/releases"
        name "SACommerce"
    }
}

// 南非特定依赖
dependencies {
    // 南非本地SDK
    implementation 'com.sacomerce:core:1.0.0'
    implementation 'com.sacomerce:pay:1.0.0'
    implementation 'com.sacomerce:logistics:1.0.0'
    
    // 南非特定库
    implementation 'com.peachpayments:android-sdk:2.0.0'  // 本地支付整合
}

// 南非特定任务
tasks.register('printSaConfig') {
    doLast {
        println "SA Configuration:"
        println "  Country: ${saConfig.country}"
        println "  Currency: ${saConfig.currency}"
        println "  Languages: ${saConfig.supportedLanguages}"
        println "  Provinces: ${saConfig.provinces.size()}"
    }
}
