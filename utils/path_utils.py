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

def get_database_conn_str() -> str:
    db_path = resource_path("database/AmericaAirsoftDataBase.accdb")
    print(f"Using DB path: {db_path}")  # DEBUG

    return (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        f'DBQ={db_path};'
        'PWD=americairsoft;'
    )


def relative_to_assets(path: str) -> Path:
    """
    Returns the absolute path to a specific file inside the assets folder.
    """
    return get_assets_path() / Path(path)
