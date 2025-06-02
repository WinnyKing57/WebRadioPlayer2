[app]

# (str) Title of your application
title = Radio App

# (str) Package name
package.name = radioapp

# (str) Package domain (needed for Android/iOS)
package.domain = org.myradio

# (str) Source code directory (current directory for this project)
source.dir = .

# (list) Source files to include (Python, Kivy, JSON data, images, etc.)
# Add other extensions if you have them (e.g., .mp3, .wav for local sounds)
source.include_exts = py,png,jpg,jpeg,gif,kv,atlas,json,txt

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let's exclude buildozer artifacts and tests if any)
source.exclude_exts = spec,ini # Exclude .spec itself, .buildozer files are usually in ./.buildozer
source.exclude_dirs = tests, bin, .buildozer, .venv, __pycache__
# source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (e.g., 0.1, 1.0, 1.2.0)
version = 0.1

# (list) Requirements of your application
# Specify versions if needed, e.g., kivy==2.3.0 or kivy~=2.3.0
# Using kivy~=2.3.0 based on subtask report where Kivy 2.3.1 was installed.
requirements = python3,kivy~=2.3.0,requests

# (str) Custom Kivy version to use (e.g., "stable", "master", "2.3.0")
# Kivy version is usually handled by the requirements line.
# kivy_version =

# (str) Presplash background color (name or #RRGGBB hexadecimal)
# presplash.color = #FFFFFF

# (str) Presplash image
# Presplash screen (displayed while Kivy is loading)
# presplash.filename = data/images/presplash.png # Example path

# (str) Icon filename
# Icon of the application
# icon.filename = data/images/icon.png # Example path

# (str) Supported orientation (one of landscape, sensorLandscape, portrait, sensorPortrait, all)
orientation = portrait

# (list) List of service to declare
# services = Name:entrypoint.py,Name2:entrypoint2.py

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Android API to use
android.api = 27 # Default is 27 (Android 8.1 Oreo), min is 21 (Android 5.0 Lollipop)
android.minapi = 21 # Minimum supported API level.

# (int) Android SDK version to use
# android.sdk = 24

# (int) Android NDK version to use
# android.ndk = 19b # Example: 19b, 21e, etc. (Often auto-detected)

# (str) Android NDK path (leave empty for auto-detection)
# android.ndk_path =

# (str) Android SDK path (leave empty for auto-detection)
# android.sdk_path =

# (str) Python for android branch to use
#p4a.branch = master # or develop, or a specific tag

# (str) Android architecture to build for (armeabi-v7a, arm64-v8a, x86, x86_64)
android.arch = armeabi-v7a # For wider compatibility, though arm64-v8a is common now

# (list) Android application meta-data to set (key=value format)
# android.meta_data = Camera=true


#
# iOS specific (not used for this APK task but good to know)
#

# (str) Name of the certificate to use for signing the debug version
# ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<id>)"

# (str) Name of the certificate to use for signing the release version
# ios.codesign.release = "iPhone Distribution: <lastname> <firstname> (<id>)"


#
# OSX specific (not used for this APK task)
#

# (str) OSX Kivy Window Manager style
# osx.𝘬𝘪𝘷𝘺_𝘸𝘪𝘯𝘥𝘰𝘸_𝘮𝘢𝘯𝘢𝘨𝘦𝘳_𝘴𝘵𝘺𝘭𝘦 = sdl2


[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build CACE (default is ~/.buildozer/cache)
# build_dir = ./.buildozer
# bin_dir = ./bin # Output directory for APKs

# The `build_dir` and `bin_dir` are usually inside the .buildozer folder which is fine.
# Default: .buildozer/android/platform/build-armeabi-v7a/dists/myappname__armeabi-v7a/bin/myappname-0.1-armeabi-v7a-debug.apk
