import os
import sys
import toml

from xdg import xdg_config_home


def canonical_config_dir():
    # on linux, use xdg_config_home
    # on windows, use appdata
    # on macos, use HOME/Library/Preferences
    if sys.platform == "linux":
        return xdg_config_home()
    elif sys.platform == "win32":
        return os.environ["APPDATA"]
    elif sys.platform == "darwin":
        return os.path.expanduser("~/Library/Preferences")


def canonical_config_base(app_name):
    return canonical_config_dir() / app_name


def canonical_config_file(app_name, config_file_name):
    return canonical_config_base(app_name) / config_file_name


class ConfigError(Exception):
    def __init__(self, message=""):
        super().__init__(message)


class TomlConfigFile:
    def get_config_section(self, section, required=False):
        if section not in self.config:
            if required:
                raise ConfigError(f"config file missing [{section}] section")
            else:
                return {}
        return self.config[section]

    def get_config_value(self, table, key, default=None, required=False):
        if key not in table:
            if required:
                raise ConfigError(f"config table {table} missing {key} key")
            else:
                return default
        return table[key]

    def load_from(self, config_path, wizard_callback=None) -> bool:
        # ensure the config file exists
        if not os.path.exists(config_path):
            # show a wizard to create the config file
            if wizard_callback:
                if not wizard_callback(config_path):
                    return False

        with open(config_path, "r") as conf_file:
            self.config = toml.load(conf_file)

        return True
