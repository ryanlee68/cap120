import pickle
from pathlib import Path

PICKLE_FILE = Path("pickle/count.pkl")

def save_int(value: int) -> None:
    with PICKLE_FILE.open("wb") as f:
        pickle.dump(value, f)

def load_int(default: int = 0) -> int:
    if not PICKLE_FILE.exists():
        return default
    with PICKLE_FILE.open("rb") as f:
        return pickle.load(f)

def count() -> None:
    count = load_int()
    count+=1
    save_int(count)

def check_count() -> bool:
    count = load_int()
    return count%2 == 0

def get_count() -> int:
    return load_int()
