// 南非跨境电商APP - Android构建配置
android {
    namespace 'com.sacomerce.app'
    compileSdk 34

    defaultConfig {
        applicationId "com.sacomerce.app"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"

        // 南非区域配置
        resConfigs "en", "af", "zu", "xh"
        
        // 支持的屏幕密度
        vectorDrawables.useSupportLibrary = true
        
        // 南非官方语言支持
        resourceConfigurations += ["en", "af", "zu", "xh", "nso", "st", "tn"]
        
        // 默认货币
        buildConfigField "String", "DEFAULT_CURRENCY", "\"ZAR\""
        buildConfigField "String", "COUNTRY_CODE", "\"ZA\""
    }

    signingConfigs {
        release {
            // 发布签名配置（需替换为实际密钥）
            storeFile file('release-keystore.jks')
            storePassword System.getenv('KEYSTORE_PASSWORD')
            keyAlias System.getenv('KEY_ALIAS')
            keyPassword System.getenv('KEY_PASSWORD')
        }
        debug {
            storeFile file('debug-keystore.jks')
            storePassword 'android'
            keyAlias 'androiddebugkey'
            keyPassword 'android'
        }
    }

    buildTypes {
        debug {
            applicationIdSuffix ".debug"
            debuggable true
            buildConfigField "String", "BASE_URL", '"https://api-staging.sacomerce.co.za"'
        }
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
            signingConfig signingConfigs.release
            buildConfigField "String", "BASE_URL", '"https://api.sacomerce.co.za"'
        }
        // 南非特定构建（本地化优化）
        zaRelease {
            initWith release
            buildConfigField "boolean", "OPTIMIZED_FOR_ZA", "true"
        }
    }

    // 多渠道打包（南非运营商定制）
    flavorDimensions += "carrier"
    productFlavors {
        defaultConfig {
            dimension "carrier"
        }
        // MTN定制版
        mtn {
            dimension "carrier"
            applicationIdSuffix ".mtn"
            buildConfigField "String", "CARRIER", "\"MTN\""
        }
        // Vodacom定制版
        vodacom {
            dimension "carrier"
            applicationIdSuffix ".vodacom"
            buildConfigField "String", "CARRIER", "\"VODACOM\""
        }
        // 通用版
        generic {
            dimension "carrier"
            buildConfigField "String", "CARRIER", "\"GENERIC\""
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = '17'
    }

    buildFeatures {
        viewBinding true
        buildConfig true
    }

    // APK输出配置
    applicationVariants.configureEach { variant ->
        variant.outputs.each { output ->
            def outputFile = output.outputFileName
            if (outputFile != null && outputFile.endsWith('.apk')) {
                def flavor = variant.flavorName ?: "default"
                def buildType = variant.buildType.name
                def version = variant.versionName
                def versionCode = variant.versionCode
                outputFileName = "SACommerce_${flavor}_${version}_${buildType}.apk"
            }
        }
    }

    // 南非特定资源
    sourceSets {
        main {
            res.srcDirs = [
                'src/main/res',
                'src/main/res-za'  // 南非特定资源
            ]
        }
    }

    // 代码混淆规则
    packaging {
        resources {
            excludes += '/META-INF/{AL2.0,LGPL2.1}'
            excludes += 'META-INF/DEPENDENCIES'
        }
    }

    lint {
        abortOnError false
        checkReleaseBuilds false
        // 忽略南非特定警告
        disable 'MissingTranslation', 'ExtraTranslation'
    }
}

dependencies {
    // AndroidX
    implementation 'androidx.core:core-ktx:1.12.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    
    // Jetpack
    implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0'
    implementation 'androidx.lifecycle:lifecycle-livedata-ktx:2.7.0'
    implementation 'androidx.navigation:navigation-fragment-ktx:2.7.6'
    implementation 'androidx.navigation:navigation-ui-ktx:2.7.6'
    
    // 网络
    implementation 'com.squareup.retrofit2:retrofit:2.9.0'
    implementation 'com.squareup.retrofit2:converter-gson:2.9.0'
    implementation 'com.squareup.okhttp3:okhttp:4.12.0'
    implementation 'com.squareup.okhttp3:logging-interceptor:4.12.0'
    
    // 图片
    implementation 'com.github.bumptech.glide:glide:4.16.0'
    
    // 本地化
    implementation 'com.google.android.gms:play-services-location:21.1.0'
    
    // 支付SDK
    implementation 'com.paystack:paystack:3.2.3'  // 南非常用支付
    implementation 'com.ozow:ozow-android:1.0.0'  // Ozow支付
    implementation 'com.paypal.sdk:android-sdk:2.15.0'  // PayPal
    
    // 安全
    implementation 'androidx.security:security-crypto:1.1.0-alpha06'
    
    // 性能
    implementation 'androidx.startup:startup-runtime:1.1.1'
}

// Gradle任务：生成南非特定APK
task buildZaRelease(type: Exec) {
    group = 'build'
    description = 'Build SA-optimized release APK'
    commandLine 'bash', '-c', './gradlew assembleZaRelease'
}

// Gradle任务：生成所有渠道APK
task buildAllCarriers(type: Exec) {
    group = 'build'
    description = 'Build all carrier-specific APKs'
    commandLine 'bash', '-c', './gradlew assembleMtnRelease assembleVodacomRelease assembleGenericRelease'
}

// Gradle任务：清理并构建
task cleanBuild(type: Exec) {
    group = 'build'
    description = 'Clean and build all variants'
    commandLine 'bash', '-c', './gradlew clean assembleDebug'
}
