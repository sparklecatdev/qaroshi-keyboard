plugins { id("com.android.application") }

android {
    namespace = "dev.qaroshi.keyboard"
    compileSdk = 35
    defaultConfig {
        applicationId = "dev.qaroshi.keyboard"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "0.2.0"
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
