[app]
# Informations basiques de l'application
title = WebRadioPy
package.name = webradiopro
package.domain = org.winny

# Source
source.dir = .
source.include_exts = py,png,jpg,kv,json,mp3,wav,ttf
source.exclude_dirs = tests,bin,.buildozer,__pycache__

# Version dynamique depuis main.py
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# Configuration UI
orientation = portrait
fullscreen = 1
android.hardwareAccelerated = 1
android.allow_backup = False

# Audio et affichage
android.wakelock = 1
android.media_volume = 1
android.background_color = #000000

# Ressources
icon.filename = assets/icon.png
presplash.filename = assets/presplash.png

# Android specifics
android.api = 34
android.minapi = 23
android.archs = armeabi-v7a, arm64-v8a
android.ndk_path = /home/runner/.android/ndk/25.2.9519653

# Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK, FOREGROUND_SERVICE

# Dépendances Python
requirements = 
    python3==3.10.12,
    kivy==2.3.0,
    requests==2.31.0,
    plyer==2.1.0,
    android,
    openssl,
    pyjnius,
    audiostream,
    ffpyplayer @ git+https://github.com/matham/ffpyplayer.git@master,
    libffi,
    numpy,
    setuptools,
    cython==0.29.36

# Options de build
p4a.branch = develop
android.enable_androidx = True
android.release_artifact = .apk
android.accept_sdk_license = True
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
ci_build = True