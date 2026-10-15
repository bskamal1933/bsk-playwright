import copy
import json
from functools import lru_cache
from pathlib import Path

DATA_DIR = Path(__file__).parent


@lru_cache(maxsize=None)
def _read(name: str) -> dict:
    return json.loads((DATA_DIR / name).read_text())


def load_json(name: str) -> dict:
    """Read a JSON file once (cached) and return a fresh copy.

    The deepcopy matters: tests may modify the data, and a shared mutable
    object would leak changes into other tests.
    """
    return copy.deepcopy(_read(name))
