import sys
from pathlib import Path
from config_loader import Configloader, ConfigValidator

def main() -> int:
    """Run the Pac-Man application."""
    if len(sys.argv) != 2:
        print("Error: expected exactly one configuration file.")
        print("Usage: python3 pac-man.py config.json")
        return 1

    config_path = Path(sys.argv[1])

    if config_path.suffix.lower() != ".json":
        print("Error: configuration file must be a JSON file.")
        return 1

    if not config_path.exists():
        print(f"Error: configuration file '{config_path}' was not found.")
        return 1

    if not config_path.is_file():
        print(f"Error: '{config_path}' is not a valid file.")
        return 1

    print(f"Configuration file accepted: {config_path}")
    conf = Configloader(config_path)
    config_data = conf.load()
    valid = ConfigValidator(config_data)
    valid.validate()
    return 0


if __name__ == "__main__":
    sys.exit(main())