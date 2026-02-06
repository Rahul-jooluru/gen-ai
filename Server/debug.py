import sys
import traceback

print("Python path:", sys.path)

try:
    print("Attempting to import config...")
    import config
    print("Config module loaded successfully")
    print("Config attributes:", dir(config))
except Exception as e:
    print(f"Error importing config: {e}")
    traceback.print_exc()

try:
    print("\nAttempting to import Config class...")
    from config import Config
    print("Config class imported successfully")
except Exception as e:
    print(f"Error importing Config class: {e}")
    traceback.print_exc()