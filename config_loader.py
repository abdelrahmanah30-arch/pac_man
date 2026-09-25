import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MIN_MAZE_SIZE = 5
MAX_MAZE_SIZE = 50

DEFAULTS: Dict[str, Any] = {
    "highscore_filename": "data/highscores.json",
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90,
}


class ConfigError(Exception):
    """Raised when the configuration file cannot be read or parsed."""


class ConfigLoader:
    """Reads a JSON configuration file that may contain comments.

    Supported comment styles, recognised outside of string literals:
        - '#' to the end of the line.
        - '//' to the end of the line.
        - '/* ... */' block comments, which may span multiple lines.
    """

    def __init__(self, config_path: Path) -> None:
        """Store the path of the configuration file to load.

        Args:
            config_path: Path to the JSON configuration file.
        """
        self.config_path = config_path

    def load(self) -> Dict[str, Any]:
        """Read, de-comment and parse the configuration file.

        Returns:
            The parsed configuration as a dictionary.

        Raises:
            ConfigError: If the file cannot be read, or is not valid
                JSON once comments have been stripped.
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as file_object:
                raw_text = file_object.read()
        except OSError as error:
            raise ConfigError(
                f"could not read configuration file "
                f"'{self.config_path}': {error}"
            ) from error

        clean_text = self._strip_comments(raw_text)

        try:
            config_data = json.loads(clean_text)
        except json.JSONDecodeError as error:
            raise ConfigError(
                f"configuration file '{self.config_path}' is not "
                f"valid JSON: {error}"
            ) from error

        if not isinstance(config_data, dict):
            raise ConfigError(
                "configuration file must contain a JSON object "
                "at its top level"
            )

        return config_data

    @staticmethod
    def _strip_comments(text: str) -> str:
        """Remove '#', '//' and '/* */' comments found outside strings.

        Args:
            text: The raw file content.

        Returns:
            The text with every comment replaced by nothing, leaving
            valid JSON (assuming the file was well-formed otherwise).
        """
        result: List[str] = []
        index = 0
        length = len(text)
        in_string = False

        while index < length:
            char = text[index]

            if in_string:
                result.append(char)
                if char == "\\" and index + 1 < length:
                    result.append(text[index + 1])
                    index += 2
                    continue
                if char == '"':
                    in_string = False
                index += 1
                continue

            if char == '"':
                in_string = True
                result.append(char)
                index += 1
                continue

            if char == "#" or text[index:index + 2] == "//":
                newline = text.find("\n", index)
                index = length if newline == -1 else newline
                continue

            if text[index:index + 2] == "/*":
                end = text.find("*/", index + 2)
                index = length if end == -1 else end + 2
                continue

            result.append(char)
            index += 1

        return "".join(result)


class ConfigValidator:
    """Validates a raw configuration dictionary and repairs bad values.

    Every scalar key is clamped to a safe default when missing or
    invalid; the game never receives an unusable configuration.
    Level size overrides are parsed separately and exposed through
    ``config_level``.
    """

    def __init__(self, config_data: Dict[str, Any]) -> None:
        """Wrap the raw configuration dictionary to be validated.

        Args:
            config_data: The dictionary produced by ConfigLoader.load().
        """
        self.config_data = config_data
        self.config_level: List[Optional[Tuple[int, int]]] = []

    def validate(self) -> None:
        """Clamp every known key in place and parse level overrides.

        After this call, ``self.config_data`` only ever contains safe,
        correctly-typed values for every known key, and
        ``self.config_level`` holds the parsed per-level size overrides
        (index 0 = level 1). An entry is ``None`` when that level has
        no valid override and should use the game's default size.
        """
        self.config_level = self._validate_levels()

        self._validate_string(
            "highscore_filename", DEFAULTS["highscore_filename"]
        )

        self._validate_int("lives", DEFAULTS["lives"], minimum=1, maximum=3)
        self._validate_int("pacgum", DEFAULTS["pacgum"], minimum=1)
        self._validate_int(
            "points_per_pacgum",
            DEFAULTS["points_per_pacgum"],
            minimum=0,
        )
        self._validate_int(
            "points_per_super_pacgum",
            DEFAULTS["points_per_super_pacgum"],
            minimum=0,
        )
        self._validate_int(
            "points_per_ghost", DEFAULTS["points_per_ghost"], minimum=0
        )
        self._validate_int("seed", DEFAULTS["seed"], minimum=0)
        self._validate_int(
            "level_max_time", DEFAULTS["level_max_time"], minimum=1
        )

    def _validate_int(
        self,
        key: str,
        default: int,
        minimum: Optional[int] = None,
        maximum: Optional[int] = None,
    ) -> None:
        """Clamp self.config_data[key] to a valid integer in place."""
        value = self.config_data.get(key, default)

        if not self._is_plain_int(value):
            print(
                f"Config warning: '{key}' must be an integer, "
                f"using default {default}"
            )
            value = default
        elif minimum is not None and value < minimum:
            print(
                f"Config warning: '{key}' is below the minimum "
                f"({minimum}), using default {default}"
            )
            value = default
        elif maximum is not None and value > maximum:
            print(
                f"Config warning: '{key}' is above the maximum "
                f"({maximum}), using default {default}"
            )
            value = default

        self.config_data[key] = value

    def _validate_string(self, key: str, default: str) -> None:
        """Clamp self.config_data[key] to a non-empty string in place."""
        value = self.config_data.get(key, default)

        if not isinstance(value, str) or not value.strip():
            print(
                f"Config warning: '{key}' must be a non-empty string, "
                f"using default '{default}'"
            )
            value = default

        self.config_data[key] = value

    def _validate_levels(self) -> List[Optional[Tuple[int, int]]]:
        """Parse the optional 'level' array of per-level size overrides."""
        raw_levels = self.config_data.get("level", [])

        if not isinstance(raw_levels, list):
            print(
                "Config warning: 'level' must be an array, "
                "ignoring level overrides"
            )
            return []

        return [
            self._validate_level_entry(index, entry)
            for index, entry in enumerate(raw_levels)
        ]

    def _validate_level_entry(
        self,
        index: int,
        entry: Any,
    ) -> Optional[Tuple[int, int]]:
        """Validate a single 'level' array entry, or reject it."""
        if not isinstance(entry, dict):
            print(
                f"Config warning: level override #{index + 1} must be "
                f"an object, using the default size"
            )
            return None

        width = entry.get("width")
        height = entry.get("height")

        if self._is_valid_maze_dimension(width) and self._is_valid_maze_dimension(height):
            return width, height

        print(
            f"Config warning: level override #{index + 1} is missing "
            f"or has an invalid width/height, using the default size"
        )
        return None

    @staticmethod
    def _is_plain_int(value: Any) -> bool:
        """Return True if value is an int and not a bool in disguise."""
        return isinstance(value, int) and not isinstance(value, bool)

    @classmethod
    def _is_valid_maze_dimension(cls, value: Any) -> bool:
        """Return True if value is a usable maze width/height."""
        return (
            cls._is_plain_int(value)
            and MIN_MAZE_SIZE <= value <= MAX_MAZE_SIZE
        )