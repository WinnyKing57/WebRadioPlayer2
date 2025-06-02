[app]

# Titre et identification
title = Radio App
package.name = radioapp
package.domain = org.myradio

# Gestion des sources
source.dir = .
source.include_exts = py,png,jpg,jpeg,gif,kv,atlas,json,txt,mp3,wav,ogg
source.exclude_exts = spec,ini,log,db
source.exclude_dirs = tests,bin,.buildozer,.venv,__pycache__,backups

# Version
version = 1.0.0
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# Configuration technique
orientation = portrait
fullscreen = 1
android.hardwareAccelerated = 1
android.allow_backup = False
android.wakelock = 1
android.media_volume = 1

# Ressources graphiques
icon.filename = icon.png
presplash.filename = presplash.png

# Spécifications Android
android.api = 34
android.minapi = 23
android.arch = arm64-v8a
# android.archs = arm64-v8a,armeabi-v7a  # Alternative multi-arch
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK, FOREGROUND_SERVICE
android.adaptive_icon_foreground = icon_foreground.png
android.adaptive_icon_background = #FFFFFF
android.enable_androidx = True
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-xxxxxxxx~yyyyyyyyyy

# Dépendances
requirements = 
    python3==3.10.12,
    kivy==2.3.0,
    requests==2.31.0,
    plyer==2.1.0,
    android,
    openssl,
    certifi,
    urllib3,
    pyjnius,
    audiostream==3.0.0,
    ffpyplayer,
    pillow

# Configuration avancée
p4a.options = --debug
p4a.branch = develop
p4a.release = False

[buildozer]

# Configuration de build
log_level = 2
warn_on_root = 1
target = android
package_type = apk

# Répertoires
build_dir = ./.buildozer
bin_dir = ./bin

# Options de débogage
debug = 1
verbose = True
android.accept_sdk_license = True

# Configuration NDK/SDK (laisser vide pour auto-détection)
# android.sdk_path = 
# android.ndk_path = 
# android.ndk_version = 25b

# Personnalisation du build
# p4a.extra_args = --service=MyService:foreground

# Hook personnalisé (optionnel)
# pre_build = python pre_build_hook.py
# post_build = python post_build_hook.py
