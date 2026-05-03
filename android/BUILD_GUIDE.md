# 南非跨境电商 APP - Android 构建指南

## 📱 项目结构

```
android/
├── app/
│   ├── build.gradle.kts          # 应用构建配置
│   ├── proguard-rules.pro        # 混淆规则
│   └── src/main/
│       ├── AndroidManifest.xml
│       ├── java/com/sacomerce/app/
│       │   ├── MainActivity.kt    # 主界面
│       │   ├── SACommerceApp.kt   # Application类
│       │   └── config/
│       │       └── SAConfig.kt    # 配置类
│       └── res/
│           ├── layout/           # 布局文件
│           ├── values/           # 字符串资源
│           └── xml/               # 配置文件
├── build.gradle.kts              # 根项目配置
├── settings.gradle.kts           # 项目设置
├── gradlew                       # Gradle wrapper (Linux/Mac)
├── gradlew.bat                   # Gradle wrapper (Windows)
└── gradle/wrapper/
    └── gradle-wrapper.properties
```

## 🔧 构建前准备

### 1. 安装 Android Studio

下载并安装最新版本的 Android Studio:
- https://developer.android.com/studio
- 安装时确保勾选 "Android SDK"

### 2. 安装 JDK

推荐使用 JDK 17:
```bash
# macOS
brew install openjdk@17

# Ubuntu/Debian
sudo apt install openjdk-17-jdk

# Windows - 从 Oracle 下载
```

### 3. 配置环境变量

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools
export JAVA_HOME=$(/usr/libexec/java_home -v 17)  # macOS
```

## 📦 构建步骤

### 方式一：Android Studio 图形界面

1. **打开项目**
   - 启动 Android Studio
   - File → Open → 选择 `android/` 文件夹
   - 等待 Gradle sync 完成

2. **配置签名**
   - File → Project Structure → Signing
   - 添加 release 签名配置

3. **构建 APK**
   - Build → Generate Signed Bundle/APK
   - 选择 APK → Release
   - 选择签名文件 → 完成

### 方式二：命令行构建

```bash
cd android

# 给 gradlew 添加执行权限
chmod +x gradlew

# 下载 Gradle wrapper (首次构建)
./gradlew wrapper

# 构建 Debug APK
./gradlew assembleDebug

# 构建 Release APK
./gradlew assembleZaRelease

# 构建所有变体
./gradlew assemble
```

### 方式三：Docker 构建（推荐 CI/CD）

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    wget \
    unzip

ENV ANDROID_HOME=/opt/android-sdk
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# 下载 Android SDK
RUN wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O /tmp/cmdline-tools.zip && \
    unzip -q /tmp/cmdline-tools.zip -d /opt/android-sdk && \
    mv /opt/android-sdk/cmdline-tools /opt/android-sdk/cmdline-tools/latest && \
    rm /tmp/cmdline-tools.zip

RUN yes | /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager --licenses || true

RUN /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager \
    "platform-tools" "platforms;android-34" "build-tools;34.0.0"

WORKDIR /app
COPY . /app

RUN chmod +x gradlew && ./gradlew assembleDebug

CMD ["cp", "app/build/outputs/apk/debug/app-debug.apk", "/output/app.apk"]
```

## ⚙️ 配置说明

### 1. API 配置

编辑 `app/src/main/java/com/sacomerce/app/config/SAConfig.kt`:

```kotlin
companion object {
    // 部署后替换为实际的 API 地址
    const val API_BASE_URL = "https://your-deployed-api.coze.cn"
    const val API_TOKEN = "your_api_token"
}
```

### 2. 应用名称

编辑 `app/src/main/res/values/strings.xml`:
```xml
<resources>
    <string name="app_name">SA Commerce</string>
</resources>
```

### 3. 签名配置

编辑 `app/build.gradle.kts`:
```kotlin
android {
    signingConfigs {
        create("release") {
            storeFile = file("keystore/your-keystore.jks")
            storePassword = "your-password"
            keyAlias = "your-alias"
            keyPassword = "your-key-password"
        }
    }
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

## 📍 构建产物

| 变体 | 文件位置 |
|------|----------|
| Debug APK | `app/build/outputs/apk/debug/app-debug.apk` |
| Release APK | `app/build/outputs/apk/za/release/app-za-release.apk` |
| App Bundle | `app/build/outputs/bundle/zaRelease/app-za-release.aab` |

## 🐛 常见问题

### 1. Gradle sync 失败

```bash
# 清理并重新同步
./gradlew clean
./gradlew --refresh-dependencies
```

### 2. SDK 找不到

```bash
# 设置 SDK 路径
export ANDROID_SDK_ROOT=$HOME/Android/Sdk
```

### 3. 签名错误

确保 keystore 文件存在且密码正确。

### 4. 网络超时

修改 `gradle.properties`:
```properties
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
systemProp.http.timeout=120
systemProp.https.timeout=120
```

## 🚀 上架 Google Play

### 1. 生成签名 APK

```bash
./gradlew assembleZaRelease
```

### 2. 生成 App Bundle (推荐)

```bash
./gradlew bundleZaRelease
```

### 3. 签署 App Bundle

```bash
# 使用 android-gradle-signing-tool 或 Android Studio
```

### 4. 提交审核

登录 Google Play Console → 创建应用 → 上传 AAB → 填写信息 → 提交审核

## 📞 获取帮助

如有问题，请参考:
- Android 官方文档: https://developer.android.com/docs
- Gradle 文档: https://docs.gradle.org
