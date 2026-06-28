[app]

# 搴旂敤鍚嶇О
title = 鑴氭湰鏂囨鐢熸垚鍣?
# 鍖呭悕
package.name = scriptgenerator
package.domain = com.example

# 婧愪唬鐮佺洰褰?source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# 鐗堟湰
version = 1.0.0
version.code = 1

# 渚濊禆
requirements = python3,kivy==2.1.0,kivymd==1.1.1,httpx,bs4,lxml,jinja2

# 鏂瑰悜
orientation = portrait

# 鍏ㄥ睆
fullscreen = 0

# Android 閰嶇疆
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk_api = 25
android.accept_sdk_licenses = True
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = True

[buildozer]

# 鏃ュ織绾у埆 (2 = DEBUG)
log_level = 2

# 鏄惁鍦?root 鐢ㄦ埛涓嬭繍琛?warn_on_root = 1
