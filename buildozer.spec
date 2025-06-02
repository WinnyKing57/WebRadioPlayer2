[app]
# Configuration de base
title = WebRadioPy
package.name = webradiopro
package.domain = org.winny

# Gestion des sources
source.dir = .
source.include_exts = py,png,jpg,kv,json,mp3,wav,ttf
source.exclude_dirs = tests,bin,.buildozer,__pycache__

# Version (méthode dynamique recommandée)
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# Configuration technique
orientation = portrait
fullscreen = 1
android.hardwareAccelerated = 1
android.allow_backup = False

# Configuration audio spécifique
android.wakelock = 1
android.media_volume = 1
android.background_color = #000000

# Ressources
#icon.filename = assets/icon.png
#presplash.filename = assets/presplash.png

# Configuration Android
android.api = 34
android.minapi = 23
android.arch = arm64-v8a

# Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK, FOREGROUND_SERVICE

# Dépendances
requirements = 
    python3==3.10.12,
    kivy==2.3.0,
    requests==2.31.0,
    plyer==2.1.0,
    android,
    openssl,
    pyjnius,
    audiostream,
    ffpyplayer

[buildozer]
log_level = 2
warn_on_root = 1
android.accept_sdk_license = True
