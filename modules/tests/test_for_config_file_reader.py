import unittest
from pathlib import Path
from unittest.mock import patch
import tomli
import tomli_w
from preteky.modules.config_file_reader import ConfigFileReader

TEST_CONFIG_FILE_PATH = Path("test_config.toml")


class TestConfigFileReader(unittest.TestCase):
    def setUp(self):
        self.config_file_path = TEST_CONFIG_FILE_PATH
        if self.config_file_path.exists():
            self.config_file_path.unlink()
        else:
            self.config_file_path.touch()

    def tearDown(self):
        if self.config_file_path.exists():
            self.config_file_path.unlink()

    @patch("sys.exit")
    def test_create_example_config(self, mock_exit):
        config_reader = ConfigFileReader(output=False, config_file_path=self.config_file_path)
        config_reader._create_example_config()
        self.assertTrue(self.config_file_path.exists(), "Config file should be created")
        with open(self.config_file_path, 'rb') as f:
            config_dict = tomli.load(f)
            self.assertIn("IS_API_KEY", config_dict)
            self.assertIn("IS_API_ENDPOINT", config_dict)

    @patch("sys.exit")
    def test_load_config(self, mock_exit):
        sample_config = {
            "IS_API_KEY": "test_api_key",
            "IS_API_ENDPOINT": "https://api.test.com",
            "SANDBERG_API_ENDPOINT": "https://sandberg.test.com",
            "GOOGLE_CREDENTIALS_PATH": "/path/to/credentials",
            "GOOGLE_EMAILS": ["test@example.com"],
            "CLUB_ID": 123,
            "HOME_DIR": "/home/user"
        }

        with open(self.config_file_path, "wb") as f:
            tomli_w.dump(sample_config, f)

        config_reader = ConfigFileReader(output=False, config_file_path=self.config_file_path)
        config_reader._load_config()

        self.assertEqual(config_reader.IS_API_KEY, "test_api_key")
        self.assertEqual(config_reader.IS_API_ENDPOINT, "https://api.test.com")
        self.assertEqual(config_reader.SANDBERG_API_ENDPOINT, "https://sandberg.test.com")
        self.assertEqual(config_reader.GOOGLE_CREDENTIALS_PATH, "/path/to/credentials")
        self.assertEqual(config_reader.GOOGLE_EMAILS, ["test@example.com"])
        self.assertEqual(config_reader.CLUB_ID, 123)
        self.assertEqual(config_reader.HOME_DIR, "/home/user")

    @patch("sys.exit")
    def test_save_config(self, mock_exit):
        config_reader = ConfigFileReader(output=False, config_file_path=self.config_file_path)
        config_reader._create_example_config()
        new_home_dir = "C:\\Users\\test\\new_home_dir"
        config_reader.set_home_dir(new_home_dir)
        config_reader._load_config()
        self.assertEqual(config_reader.HOME_DIR, new_home_dir)

        with open(self.config_file_path, 'rb') as f:
            config_dict = tomli.load(f)
            self.assertEqual(config_dict["HOME_DIR"], new_home_dir)

    @patch("sys.exit")
    def test_missing_keys_in_config(self, mock_exit):
        sample_config = {
            "IS_API_KEY": "test_api_key",
            "IS_API_ENDPOINT": "https://api.test.com",
            "SANDBERG_API_KEY": "test_sandberg_key"
        }

        with open(self.config_file_path, "wb") as f:
            tomli_w.dump(sample_config, f)

        config_reader = ConfigFileReader(output=False, config_file_path=self.config_file_path)
        config_reader._load_config()
        with open(self.config_file_path, 'rb') as f:
            config_dict = tomli.load(f)
            self.assertIn("GOOGLE_CREDENTIALS_PATH", config_dict)
            self.assertIn("GOOGLE_EMAILS", config_dict)

    @patch("sys.exit")
    def test_empty_config_file(self, mock_exit):
        with open(self.config_file_path, "wb") as f:
            tomli_w.dump({}, f)

        config_reader = ConfigFileReader(output=False, config_file_path=self.config_file_path)
        config_reader._load_config()
        with open(self.config_file_path, 'rb') as f:
            config_dict = tomli.load(f)
            self.assertIn("GOOGLE_CREDENTIALS_PATH", config_dict)
            self.assertIn("GOOGLE_EMAILS", config_dict)

    @patch("sys.exit")
    def test_home_dir_change(self, mock_exit):
        config_reader = ConfigFileReader(output=False, config_file_path=self.config_file_path)
        config_reader._create_example_config()

        new_home_dir = "C:\\Users\\test\\new_home_dir"
        config_reader.set_home_dir(new_home_dir)

        with open(self.config_file_path, 'rb') as f:
            config_dict = tomli.load(f)
            self.assertEqual(config_dict["HOME_DIR"], new_home_dir)


if __name__ == "__main__":
    unittest.main()
