[app]
title = Phone Controller
package.name = phonecontroller
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,pyjnius,android
orientation = portrait
osx.kivy_version = 2.0.0
fullscreen = 0
android.permissions = RECORD_AUDIO, FOREGROUND_SERVICE, INTERNET, WAKE_LOCK, SYSTEM_ALERT_WINDOW
android.accept_sdk_license = True
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
