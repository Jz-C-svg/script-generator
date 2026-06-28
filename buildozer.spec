[app]

title = 鑴氭湰鏂囨鐢熸垚鍣?package.name = scriptgenerator
package.domain = com.app

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0

requirements = python3,kivy==2.1.0,kivymd==1.1.1,httpx,bs4,lxml

orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.1.0

fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk_api = 25
android.accept_sdk_license = True

android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True
android.icon = icon.png

[buildozer]

log_level = 2

warn_on_root = 1
