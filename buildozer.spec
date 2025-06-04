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
    ffpyplayer @ git+https://github.com/matham/ffpyplayer.git@e8928e9de49c7528fc801c5b3fc9f9265452e722,
    libffi,
    numpy,
    setuptools,
    cython==0.29.36,zlib,Pillow==9.5.0

# Options de build
p4a.branch = v2024.01.21
android.enable_androidx = True
android.release_artifact = .aab
android.accept_sdk_license = True
android.logcat_filters = *:S python:D

# Keystore settings - will be overridden by environment variables in CI
android.release_keystore_file = ./android.keystore
android.release_keystore_password = android
android.release_key_alias = androidkey
android.release_key_password = android

[buildozer]
log_level = 2
warn_on_root = 1
ci_build = True