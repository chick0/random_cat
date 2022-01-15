from io import BytesIO
from os import listdir
from os.path import join
from os.path import isfile
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


def get_type(cid_or_image: str or bytes) -> str or None:
    if isinstance(cid_or_image, str):
        image = search(cid=cid_or_image)
    else:
        image = cid_or_image

    if image is None:
        return None

    head = image[:6]
    mimetype = "application/octet-stream"

    if b"PNG" in head:
        mimetype = "image/png"
    elif b"GIF" in head:
        mimetype = "image/gif"
    elif "ffd8" in head.hex():
        mimetype = "image/jpeg"

    return mimetype


def get_type_and_image(cid: str) -> (str, bytes) or (None, None):
    image = search(cid=cid)

    if image is None:
        return None, None

    return get_type(image[:6]), BytesIO(image)
