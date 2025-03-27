from pathlib import Path

# Locate the config file relative to main.py
CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.txt"

def get_assets_path():
    """Reads config.txt to get the assets folder path."""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("ASSETS_PATH="):
                    return Path(line.strip().split("=", 1)[1])

        print("Error: ASSETS_PATH not found in config file.")
        return None
    except FileNotFoundError:
        print("Error: Config file not found.")
        return None
    except Exception as e:
        print(f"Error reading config file: {e}")
        return None

def get_database_conn_str():
    """Reads config.txt and returns the database connection string."""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("DATABASE_PATH="):
                    database_path = Path(line.strip().split("=", 1)[1])
                    return (
                        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                        f'DBQ={database_path};'
                    )

        print("Error: DATABASE_PATH not found in config file.")
        return None
    except FileNotFoundError:
        print("Error: Config file not found.")
        return None
    except Exception as e:
        print(f"Error reading config file: {e}")
        return None

def relative_to_assets(path: str) -> Path:
    """Returns the absolute path by joining the given relative path with ASSETS_PATH."""
    return get_assets_path() / Path(path)
