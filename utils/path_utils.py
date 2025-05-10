from pathlib import Path
import sys

def resource_path(relative_path: str) -> Path:
    """
    Returns absolute path to resource, working in both development and PyInstaller .exe
    """
    try:
        # When running as a PyInstaller bundle (_MEIPASS is a temp folder with extracted files)
        base_path = Path(sys._MEIPASS)
    except AttributeError:
        # When running from source
        base_path = Path(__file__).resolve().parent.parent

    return base_path / relative_path

def get_assets_path() -> Path:
    """
    Returns the absolute path to the 'assets' folder.
    """
    return resource_path("assets")

import shutil

def get_database_conn_str() -> str:
    # Original bundled path (read-only in PyInstaller)
    source_path = resource_path("database/AmericaAirsoftDataBase.accdb")

    # Writable copy path (current working directory)
    target_path = Path.cwd() / "AmericaAirsoftDataBase_runtime.accdb"

    # Copy once if it doesn't already exist
    if not target_path.exists():
        try:
            shutil.copy2(source_path, target_path)
            print(f"Copied DB to {target_path}")
        except Exception as e:
            print(f"Failed to copy database: {e}")

    return (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        f'DBQ={target_path};'
        'PWD=americairsoft;'
    )

def relative_to_assets(path: str) -> Path:
    """
    Returns the absolute path to a specific file inside the assets folder.
    """
    return get_assets_path() / Path(path)
