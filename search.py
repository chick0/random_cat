from os.path import join
from os.path import isfile
from os import listdir
from random import choice


def full() -> list:
    return [x for x in listdir(join("cat")) if not x.endswith(".txt")]


def random() -> str or None:
    try:
        return choice(full())
    except IndexError:
        return None


def search(cid: str) -> bytes or None:
    pt = join("cat", cid)
    if isfile(pt):
        with open(pt, mode="rb") as cat_loader:
            return cat_loader.read()

    return None
