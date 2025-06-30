import json
import os

MEMORY_FILE = "aiko_memory.json"

default_memory = {
    "name": "",
    "likes": [],
    "mood": "neutral",
    "annoyed": 0
}

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try:
                data = json.load(f)
                # Ensure all keys exist
                for key in default_memory:
                    if key not in data:
                        data[key] = default_memory[key]
                return data
            except json.JSONDecodeError:
                return default_memory.copy()
    else:
        return default_memory.copy()

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)