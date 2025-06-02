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
source.include_exts = py,png,jpg,jpeg,gif,kv,atlas,json,txt,mp3,wav

# (list) Source files to exclude
source.exclude_exts = spec,ini
source.exclude_dirs = tests, bin, .buildozer, .venv, __pycache__

# (str) Application version
version = 0.1

# (list) Application requirements
requirements = python3,kivy~=2.3.0,requests,plyer,setuptools,six,hostpython3

# (str) Supported orientation (portrait, landscape, all, etc.)
orientation = portrait

# (bool) Fullscreen mode (1=yes, 0=no)
fullscreen = 1

# (str) Icon filename
icon.filename = icon.png

# (str) Presplash image (optional)
# presplash.filename = presplash.png

# (list) Permissions
android.permissions = INTERNET

# (int) Android API to use (set to 33 for modern support)
android.api = 33

# (int) Minimum Android API supported
android.minapi = 21

# (str) Android architecture (use arm64-v8a for 64-bit or armeabi-v7a for max compatibility)
android.arch = armeabi-v7a

# (list) Filters to apply in the logcat output (useful for debugging)
android.logcat_filters = *:S python:D

# (bool) Enable Android x86 builds (optional, default is false)
# android.enable_x86 = False

# (list) Android application meta-data to set (key=value format)
# android.meta_data = 

# (bool) Android hardware acceleration (recommended for media apps)
android.hardwareAccelerated = 1

# (str) Entry point for the application (default is main.py)
# entrypoint = main.py

# (str) Environment variables to export into the build
# environment_variables = 

# (str) Package inclusion/exclusion options
# android.add_src = 
# android.add_jars = 
# android.add_aars = 

#
# iOS specific
#

# (str) iOS certificate
# ios.codesign.debug = 
# ios.codesign.release = 

#
# OSX specific
#

# (str) OSX Kivy Window Manager style
# osx.kivy_window_manager_style = sdl2


[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Directory to store the build (default is ~/.buildozer)
# build_dir = ./.buildozer

# (str) Directory where the final APK is stored
# bin_dir = ./bin

# (str) Android SDK path (usually auto-detected)
# android.sdk_path = 

# (str) Android NDK path (usually auto-detected)
# android.ndk_path = 

# (str) Additional command line args passed to p4a
# p4a.extra_args = 

# (bool) Enable verbose output during build
# verbose = 1
