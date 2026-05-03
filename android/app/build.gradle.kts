plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.sacomerce.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.sacomerce.app"
        minSdk = 24
        targetSdk = 34
        versionCode = 100
        versionName = "1.0.0"
        
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        
        vectorDrawables {
            useSupportLibrary = true
        }
        
        // 南非区配置
        buildConfigField("String", "COUNTRY_CODE", "\"ZA\"")
        buildConfigField("String", "DEFAULT_CURRENCY", "\"ZAR\"")
        buildConfigField("String", "DEFAULT_LANGUAGE", "\"en\"")
        buildConfigField("String", "CURRENCY_SYMBOL", "\"R\"")
        buildConfigField("String", "DECIMAL_SEPARATOR", "\".\"")
        buildConfigField("String", "THOUSAND_SEPARATOR", "\",\"")
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
        debug {
            isMinifyEnabled = false
        }
    }

    flavorDimensions += "region"
    productFlavors {
        create("generic") {
            dimension = "region"
            applicationIdSuffix = ""
        }
        create("mtn") {
            dimension = "region"
            applicationIdSuffix = ".mtn"
        }
        create("vodacom") {
            dimension = "region"
            applicationIdSuffix = ".vodacom"
        }
        create("za") {
            dimension = "region"
            applicationIdSuffix = ".za"
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        viewBinding = true
        buildConfig = true
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    // Android Core
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    implementation("androidx.activity:activity-ktx:1.8.2")
    implementation("androidx.fragment:fragment-ktx:1.6.2")
    
    // RecyclerView
    implementation("androidx.recyclerview:recyclerview:1.3.2")
    
    // CardView
    implementation("androidx.cardview:cardview:1.0.0")
    
    // SwipeRefreshLayout
    implementation("androidx.swiperefreshlayout:swiperefreshlayout:1.1.0")
    
    // Lifecycle
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0")
    implementation("androidx.lifecycle:lifecycle-livedata-ktx:2.7.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    
    // Navigation
    implementation("androidx.navigation:navigation-fragment-ktx:2.7.6")
    implementation("androidx.navigation:navigation-ui-ktx:2.7.6")
    
    // WorkManager - 后台任务
    implementation("androidx.work:work-runtime-ktx:2.9.0")
    
    // Startup - 初始化
    implementation("androidx.startup:startup-runtime:1.1.1")
    
    // Security - 加密存储
    implementation("androidx.security:security-crypto:1.1.0-alpha06")
    
    // WebKit
    implementation("androidx.webkit:webkit:1.10.0")
    
    // 支付SDK
    implementation("com.paystack:paystack:3.2.3")
    implementation("com.ozow:ozow-android:1.0.0")
    implementation("com.paypal.sdk:android-sdk:2.15.0")
    
    // 网络
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
    
    // JSON解析
    implementation("com.google.code.gson:gson:2.10.1")
    
    // Kotlinx Serialization
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.2")
    
    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    
    // 测试
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
}
