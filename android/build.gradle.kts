// 南非跨境电商APP - 根项目构建配置
plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.21" apply false
    id("com.google.gms.google-services") version "4.4.0" apply false
    id("org.jetbrains.kotlin.plugin.serialization") version "1.9.21" apply false
}

// 南非区版本号配置
extra.apply {
    set("VERSION_MAJOR", 1)
    set("VERSION_MINOR", 0)
    set("VERSION_PATCH", 0)
    set("COUNTRY_CODE", "ZA")
    set("DEFAULT_CURRENCY", "ZAR")
    set("DEFAULT_LANGUAGE", "en")
    set("MIN_SDK", 24)
    set("TARGET_SDK", 34)
    set("COMPILE_SDK", 34)
}
