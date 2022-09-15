"""
response_generation.response_strings

By default, uses `english.json` file inside the `response_messages` response_generation folder.

If language changes, set `response_generation.main.default_locale` and run `response_generation.main.refresh()`.
"""
import json
from pathlib import Path

from src.utils.color_logging.main import logger


default_locale: str = "en"
cached_strings: dict = {}

current_dir: Path = Path(__file__).parent
json_responses_dir: Path = Path.joinpath(current_dir, "response_messages")
json_file: Path = Path.joinpath(json_responses_dir, f"{default_locale}.json")


def refresh_response_strings():
    logger.info("Refreshing response strings...")
    global cached_strings
    with open(json_file) as f:
        cached_strings = json.load(f)
    logger.info("Refresh is done.")


def get_text(name):
    return cached_strings[name]


refresh_response_strings()
