# 南非跨境电商APP - ProGuard混淆规则

# ==================== 基础规则 ====================
-keepattributes Signature
-keepattributes *Annotation*
-keepattributes SourceFile,LineNumberTable
-keepattributes Exceptions,InnerClasses

# ==================== 通用SDK ====================

# Retrofit
-keepattributes Signature, InnerClasses, EnclosingMethod
-keepattributes RuntimeVisibleAnnotations, RuntimeVisibleParameterAnnotations
-keepclassmembers,allowshrinking,allowobfuscation interface * {
    @retrofit2.http.* <methods>;
}
-dontwarn org.codehaus.mojo.animal_sniffer.IgnoreJRERequirement
-dontwarn javax.annotation.**
-dontwarn kotlin.Unit
-dontwarn retrofit2.KotlinExtensions
-dontwarn retrofit2.KotlinExtensions$*
-if interface * { @retrofit2.http.* <methods>; }
-keep,allowobfuscation interface <1>

# OkHttp
-dontwarn okhttp3.**
-dontwarn okio.**
-dontwarn javax.annotation.**
-keepnames class okhttp3.internal.publicsuffix.PublicSuffixDatabase

# Gson
-keepattributes Signature
-keepattributes *Annotation*
-dontwarn sun.misc.**
-keep class com.google.gson.** { *; }
-keep class * implements com.google.gson.TypeAdapterFactory
-keep class * implements com.google.gson.JsonSerializer
-keep class * implements com.google.gson.JsonDeserializer
-keepclassmembers,allowobfuscation class * {
  @com.google.gson.annotations.SerializedName <fields>;
}

# ==================== 业务模型 ====================
-keep class com.sacomerce.app.data.model.** { *; }
-keep class com.sacomerce.app.data.response.** { *; }

# ==================== 支付SDK ====================

# PayStack (南非)
-keep class com.paystack.** { *; }
-dontwarn com.paystack.**

# Ozow (南非本地支付)
-keep class com.ozow.** { *; }
-dontwarn com.ozow.**

# PayPal
-keep class com.paypal.** { *; }
-dontwarn com.paypal.**
-keep class io.card.** { *; }

# ==================== 微信/支付宝（跨境） ====================
-keep class com.alipay.** { *; }
-keep class com.tencent.mm.** { *; }
-dontwarn com.alipay.**
-dontwarn com.tencent.mm.**

# ==================== 地图/定位 ====================
-keep class com.google.android.gms.location.** { *; }
-dontwarn com.google.android.gms.**

# ==================== 加密相关 ====================
-keep class javax.crypto.** { *; }
-keep class java.security.** { *; }
-keep class androidx.security.crypto.** { *; }

# ==================== 反射规则 ====================
-keepclassmembers class * {
    @com.google.gson.annotations.SerializedName <fields>;
}
-keepclassmembers class * {
    @com.google.gson.annotations.Expose <fields>;
}

# ==================== 南非本地化 ====================
-keep class com.sacomerce.app.locale.** { *; }
-keep class com.sacomerce.app.i18n.** { *; }

# ==================== 性能优化 ====================
-dontwarn com.bumptech.glide.**
-keep public class * implements com.bumptech.glide.module.GlideModule
-keep class * extends com.bumptech.glide.module.AppGlideModule {
 <init>(...);
}
-keep public enum com.bumptech.glide.load.ImageHeaderParser$** {
  **[] $VALUES;
  public *;
}
-keep class com.bumptech.glide.load.data.ParcelFileDescriptorRewinder$InternalRewinder {
  *** rewind();
}

# ==================== 调试/日志 ====================
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}
-assumenosideeffects class org.slf4j.Logger {
    public static *** debug(...);
    public static *** trace(...);
}

# ==================== 资源混淆 ====================
-keepclassmembers class **.R$* {
    public static <fields>;
}

# ==================== 第三方库 ====================
-dontwarn org.jetbrains.annotations.**
-dontwarn org.conscrypt.**
-dontwarn org.openjsse.**
