import sys
from dataclasses import dataclass, asdict, field, fields
import tomli
import tomli_w
from pathlib import Path

DEFAULT_CONFIG_FILE_PATH = Path("config.toml")


@dataclass(init=False)
class ConfigFileReader:
    IS_API_KEY: str = field(repr=False, default="")
    IS_API_ENDPOINT: str = field(default="https://is.orienteering.sk/api")
    SANDBERG_API_KEY: str = field(default="", init=False)
    SANDBERG_API_ENDPOINT: str = field(default="https://senzor.robotika.sk/sks/api.php/api")
    GOOGLE_CREDENTIALS_PATH: str = field(default="")
    GOOGLE_EMAILS: list = field(default_factory=list)
    CLUB_ID: int = field(repr=False, default=81)
    HOME_DIR: str = field(default="")

    def __init__(self, output=True, config_file_path=DEFAULT_CONFIG_FILE_PATH):
        self.config_file_path = config_file_path
        self.output = output
        self.GOOGLE_EMAILS = []
        self._load_config()

    def _create_example_config(self):
        if not self.config_file_path.is_file():
            self.config_file_path.touch(mode=0o640, exist_ok=True)
            self._save_config()
        exit_msg = (
            f"Config file {self.config_file_path} was created."
        )
        sys.exit(exit_msg)

    def _load_config(self):
        if not self.config_file_path.is_file():
            self._create_example_config()
        with open(self.config_file_path, 'rb') as f:
            config_dict = tomli.load(f)
            missing_keys = False
            for fld in fields(self):
                if fld.name not in config_dict:
                    missing_keys = True
                    break
                setattr(self, fld.name, config_dict[fld.name])
            if missing_keys:
                self._save_config()

    def _save_config(self):
        with open(self.config_file_path, "wb") as f:
            tomli_w.dump(asdict(self), f)

    def set_home_dir(self, path: str):
        self.HOME_DIR = path
        self._save_config()


configuration = ConfigFileReader()
configuration.set_home_dir("C:\\Users\\miria\\Desktop\\TIS_programy\\komunikacia_sandberg\\classes\\correct_cleaner")
