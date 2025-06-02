[app]

# Titre et identification
title = Radio App
package.name = radioapp
package.domain = org.myradio

# Gestion des sources
source.dir = .
source.include_exts = py,png,jpg,jpeg,gif,kv,atlas,json,txt,mp3,wav,ogg,ttf
source.exclude_exts = spec,ini,log,db,md,yml
source.exclude_dirs = tests,bin,.buildozer,.venv,__pycache__,backups,assets/old

# Gestion de version (choisir UNE méthode)
## Méthode recommandée : version dynamique
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py
# version = 1.0.0  # À commenter si vous utilisez version.regex

# Configuration technique
orientation = portrait
fullscreen = 1
android.hardwareAccelerated = 1
android.allow_backup = False
android.wakelock = 1
android.media_volume = 1
android.background_color = #000000

# Ressources graphiques
icon.filename = assets/icon.png
presplash.filename = assets/presplash.png
android.adaptive_icon_foreground = assets/icon_foreground.png
android.adaptive_icon_background = #2C3E50

# Spécifications Android
android.api = 34
android.minapi = 23
android.arch = arm64-v8a
# android.archs = arm64-v8a,armeabi-v7a  # Décommenter pour builds multi-arch

# Permissions
android.permissions = 
    INTERNET,
    ACCESS_NETWORK_STATE,
    ACCESS_WIFI_STATE,
    WAKE_LOCK,
    FOREGROUND_SERVICE,
    RECORD_AUDIO,
    MODIFY_AUDIO_SETTINGS

# Métadonnées
android.meta_data = 
    com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-xxxxxxxx~yyyyyyyyyy
    android.app.background_running=true
    android.usesCleartextTraffic=true

# Dépendances principales
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
    audiostream>=3.0.0,
    ffpyplayer>=4.3.2,
    pillow>=10.0.0,
    kivymd==1.1.1,  # Si vous utilisez KivyMD
    androidstorage4kivy>=0.1.3  # Pour un meilleur stockage

# Configuration avancée
p4a.options = 
    --debug
    --orientation=portrait
    --enable-androidx
    --depend=androidx.appcompat:appcompat:1.6.1

p4a.branch = develop
p4a.release = False
android.enable_androidx = True
android.enable_jetifier = True

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

# Configuration NDK/SDK
# android.sdk_path = 
# android.ndk_path = 
# android.ndk_version = 25b

# Personnalisation du build
p4a.extra_args = 
    --service=MyService:foreground  # Décommenter si service en arrière-plan
    --add-source=src/

# Hooks personnalisés
pre_build = python scripts/pre_build.py  # Créer ce fichier si nécessaire
post_build = python scripts/post_build.py  # Créer ce fichier si nécessaire

# Signature (décommenter pour les versions release)
# android.release_keystore = keystore.jks
# android.release_storepassword = "password"
# android.release_keyalias = "keyalias"
# android.release_keypassword = "password"
