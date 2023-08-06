from pathlib import Path
import os


def config_directory():
    path = Path(os.path.expanduser("~/.phasor-generator/config"))
    if not path.exists():
        path.mkdir(parents=True)
    return path


def images_directory():
    path = Path(os.path.expanduser("~/.phasor-generator/images"))
    if not path.exists():
        path.mkdir(parents=True)
    return path
