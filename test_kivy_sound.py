try:
    from kivy.core.sound import SoundLoader
    print("Successfully imported SoundLoader from kivy.core.sound")
    if SoundLoader:
        print(f"SoundLoader object: {SoundLoader}")
        print(f"Available audio loaders: {SoundLoader.loaders}")
except ImportError as e:
    print(f"Failed to import kivy.core.sound: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

import kivy
print(f"Kivy version: {kivy.__version__}")
print(f"Kivy path: {kivy.__path__}")

import sys
print(f"Python sys.path: {sys.path}")
