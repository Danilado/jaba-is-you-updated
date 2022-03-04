import os, os.path
from pathlib import Path

for file in os.listdir("."):
    if os.path.isfile(file):
        file = Path(file)
        if "py" in file.suffix:
            continue
        os.replace(file.resolve(), "./" + file.name.replace('water', 'lava'))