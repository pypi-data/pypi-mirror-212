from pathlib import Path
import platform
from typing import Any
from datetime import datetime
import tomlkit

class ConfigManager():
    """Handle all the config and log files"""

    def __init__(self, app_name: str, config_directory_path: Path | None) -> None:
        self.app_name: str = app_name
        self.config_directory_path: Path = config_directory_path

        if self.config_directory_path == None:
            self.config_directory_path = self.get_default_config_path()

        self.config_file_path = Path(self.config_directory_path, 'config.toml')

        self.logs_directory_path = Path(self.config_directory_path, 'logs')
        datetime_now: datetime = datetime.now()
        datetime_format: str = f'{datetime_now.day}{datetime_now.month}{datetime_now.year}{datetime_now.hour}{datetime_now.minute}{datetime_now.second}'
        self.log_file_path = Path(self.logs_directory_path, f'{datetime_format}.log')

        self.logs_directory_path.mkdir(parents=True, exist_ok=True)

        log_files: list[Path] = list(self.logs_directory_path.iterdir())

        # Get all the files that can be log files
        valid_log_files: list[Path] = list(filter(lambda file: file.suffix == '.log', log_files))

        # Disjoint from the log files set all the files that are valid files to get the invalid ones
        invalid_log_files: list[Path] = list(set(log_files)^set(valid_log_files))

        # Remove all invalid files and all the valid files except the last 4
        for log_file in valid_log_files[:-4:] + invalid_log_files:
            log_file.unlink()

        self.log_file_path.touch(exist_ok=True)

    def get_default_config_path(self) -> Path:
        """Get the default config path according the OS"""

        if platform.system() == 'Windows':
            return Path(
                Path.home(),
                'AppData',
                'Roaming',
                self.app_name,
            )

        return Path(
            Path.home(),
            '.config',
            self.app_name,
            )

    def get_value_by_key(self, key: str) -> Any | None:
        """
        Reads the configuration file and returns the value to the desired key.
        Return None if the value is not found or the configuration file does not exists.
        """

        if not self.config_file_path.is_file():
            return None
    
        with open(self.config_file_path, 'r') as file:
            try:
                config_data: dict = tomlkit.parse(file.read())
                return config_data[key]
            except (tomlkit.exceptions.NonExistentKey, tomlkit.exceptions.UnexpectedCharError):
                return None

    def set_value_by_key(self, key: str, value: Any) -> None:
        """Write in the configuration file the given value in the desired key."""

        self.config_directory_path.mkdir(parents=True, exist_ok=True)
        self.config_file_path.touch(exist_ok=True)
    
        with open(self.config_file_path, 'r+') as file:
            config_data: dict = tomlkit.parse(file.read())

            config_data[key] = value

            file.seek(0)
            file.write(tomlkit.dumps(config_data))
            file.truncate()

    def write_into_log(self, message: str) -> None:
        """Write to the correspond log file the given message"""

        self.log_file_path.touch(exist_ok=True)

        with open(self.log_file_path, 'a') as file:
            file.write(message + '\n')
