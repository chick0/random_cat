from flask import Flask
from flask import jsonify
from flask import send_file
from flask import redirect

from search import random
from search import get_type
from search import get_type_and_image

app = Flask(__name__)


@app.get("/")
def index():
    return redirect("https://github.com/chick0/random_cat#random-cat")


@app.get("/cat")
def cat():
    cid = random()
    if cid is None:
        return jsonify({
            "error": "cat is empty"
        }), 404

    mimetype = get_type(cid_or_image=cid)

    return jsonify({
        "id": cid,
        "t": mimetype
    })


@app.get("/cat/<string:cid>")
@app.get("/cat/<string:cid>/<string:fake_path>")
def raw_cat(cid: str, fake_path: str = "None"):
    return return_cat(cid=cid)


@app.get("/meow")
@app.get("/meow/<string:fake_path>")
def meow(fake_path: str = "None"):
    cid = random()
    if cid is None:
        return jsonify({
            "error": "cat is empty"
        }), 404

    return return_cat(cid=cid)


def return_cat(cid):
    mimetype, image = get_type_and_image(cid=cid)

    if image is None:
        return jsonify({
            "error": "cat not found"
        }), 404

    name = {
        "image/png": "cat.png",
        "image/gif": "cat.gif",
        "image/jpeg": "cat.jpg",
    }.get(mimetype, "unknown")

    return send_file(
        path_or_file=image,
        attachment_filename=name,
        mimetype=mimetype
    )
