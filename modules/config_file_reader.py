import sys
from dataclasses import dataclass, asdict, field
import toml
from pathlib import Path

DEFAULT_CONFIG_FILE_PATH = Path("modules/config.toml")


@dataclass
class ConfigFileReader:
    IS_API_KEY: str = field(repr=False, default="")
    IS_API_ENDPOINT: str = "https://is.orienteering.sk/api"
    SANDBERG_API_ENDPOINT: str = "https://senzor.robotika.sk/sks/api.php/api"
    GOOGLE_CREDENTIALS_PATH: str = ""
    GOOGLE_EMAILS: str = ""
    CLUB_ID: int = field(repr=False, default=46)
    HOME_DIR: str = ""

    def __init__(self, config_file_path=DEFAULT_CONFIG_FILE_PATH, output=True):
        self.config_file_path = config_file_path
        self.output = output
        self._load_or_create_config()

    def _load_or_create_config(self):
        if self.config_file_path.is_file():
            self._load_config()
        else:
            self._save_config()
            sys.exit(f"Config file {self.config_file_path} was created. Please edit it and restart the program.")

    def _load_config(self):
        config_dict = toml.load(self.config_file_path)
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def _save_config(self):
        with open(self.config_file_path, "w") as f:
            toml.dump(asdict(self), f)

    def set_home_dir(self, path: str):
        self.HOME_DIR = path
        self._save_config()
