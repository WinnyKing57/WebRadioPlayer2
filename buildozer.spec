[app]
# Informations basiques de l’application
title = WebRadioPy
package.name = webradiopro
package.domain = org.winny

# Source
source.dir = .
source.include_exts = py,png,jpg,kv,json,mp3,wav,ttf
source.exclude_dirs = tests,bin,.buildozer,__pycache__

# Version dynamique depuis main.py (doit contenir __version__ = 'x.y.z')
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
android.arch = arm64-v8a

# Permissions nécessaires
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK, FOREGROUND_SERVICE

# Dépendances Python (versions fixes pour plus de stabilité)
requirements = python3==3.10.12, kivy==2.3.0, requests==2.31.0, plyer==2.1.0, android, openssl, pyjnius, audiostream, ffpyplayer

# Ne pas utiliser d'interface graphique pour la compilation sur CI
android.logcat_filters = *:S python:D

# SDK license acceptance automatique
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1