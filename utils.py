import pickle
from pathlib import Path
import os

os.makedirs("pickle", exist_ok=True)
COUNT_PICKLE_FILE = Path("pickle/count.pkl")

def save_last_slot(value: tuple) -> None:
    SLOT_PICKLE_FILE = Path(f"pickle/last_slot{value[1][0]}.pkl")
    with SLOT_PICKLE_FILE.open("wb") as f:
        pickle.dump(value, f)

def get_last_slot(zone) -> tuple:
    SLOT_PICKLE_FILE = Path(f"pickle/last_slot{zone}.pkl")
    if not SLOT_PICKLE_FILE.exists():
        return ([],(-1,-1))
    with SLOT_PICKLE_FILE.open("rb") as f:
        try:
            return pickle.load(f)
        except EOFError: 
            return ([],(-1,-1))
    

def save_int(value: int) -> None:
    with COUNT_PICKLE_FILE.open("wb") as f:
        pickle.dump(value, f)

def get_count(default: int = 0) -> int:
    if not COUNT_PICKLE_FILE.exists():
        return default
    with COUNT_PICKLE_FILE.open("rb") as f:
        try:
            return pickle.load(f)
        except EOFError:
            return default

def count() -> None:
    count = get_count()
    count+=1
    save_int(count)

def check_count() -> bool:
    count = get_count()
    return count%2 == 0

