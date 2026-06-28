[app]

title = Script Generator
package.name = scriptgenerator
package.domain = com.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0.0
version.code = 1

requirements = python3,kivy==2.1.0,kivymd==1.1.1,httpx,bs4,lxml,jinja2

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk_api = 25
android.accept_sdk_licenses = True
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = True

[buildozer]

log_level = 2

warn_on_root = 1
