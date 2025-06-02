print("Attempting to import plyer...")
try:
    import plyer
    print("Successfully imported plyer.")
    print(f"Plyer path: {plyer.__path__}")

    print("\nAttempting to import plyer.theme...")
    from plyer import theme as plyer_theme_test
    print("Successfully imported plyer.theme as plyer_theme_test.")
    if plyer_theme_test:
        print(f"plyer_theme_test object: {plyer_theme_test}")
        try:
            theme_val = plyer_theme_test.get_theme()
            print(f"plyer_theme_test.get_theme() returned: {theme_val}")
        except NotImplementedError:
            print("plyer_theme_test.get_theme(): Not implemented for this platform.")
        except Exception as e_get:
            print(f"Error calling plyer_theme_test.get_theme(): {e_get}")
    else:
        print("plyer_theme_test is None after import.")

except ImportError as e_imp:
    print(f"ImportError: {e_imp}")
except Exception as e_other:
    print(f"Other Exception: {e_other}")

import sys
print(f"\nPython sys.path: {sys.path}")
