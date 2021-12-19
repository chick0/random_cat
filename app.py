from io import BytesIO

from flask import Flask
from flask import jsonify
from flask import send_file

from search import random
from search import search

app = Flask(__name__)


@app.get("/")
def index():
    github = "https://github.com/chick0/random_cat"
    readme = "https://github.com/chick0/random_cat/blob/master/README.md"
    style = "display:block;margin:auto;text-align:center;text-decoration:none;color:#5f5e5e;"
    return "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n" + \
           f"<a href=\"{github}\" style=\"{style}font-size:80px;padding-top:33px\" target=\"_blank\">Github</a><br>" + \
           f"<a href=\"{readme}\" style=\"{style}font-size:35px\" target=\"_blank\">or README.md</a><br>" + \
           "<center>🐱 is ❤️ </center>"


@app.get("/cat")
def cat():
    cid = random()
    if cid is None:
        return jsonify({
            "error": "cat is empty"
        }), 404

    return jsonify({
        "id": cid
    })


@app.get("/cat/<string:cid>")
def raw_cat(cid: str):
    return return_cat(cid=cid)


@app.get("/meow")
def meow():
    cid = random()
    if cid is None:
        return jsonify({
            "error": "cat is empty"
        }), 404

    return return_cat(cid=cid)


def return_cat(cid):
    img_or_none = search(cid=cid)

    if img_or_none is None:
        return jsonify({
            "error": "cat not found"
        }), 404

    if b"PNG" in img_or_none[:6]:
        return send_file(
            path_or_file=BytesIO(img_or_none),
            attachment_filename="cat.png",
            mimetype="image/png"
        )
    elif b"GIF" in img_or_none[:6]:
        return send_file(
            path_or_file=BytesIO(img_or_none),
            attachment_filename="cat.gif",
            mimetype="image/gif"
        )
    elif "ffd8" in img_or_none[:4].hex():
        return send_file(
            path_or_file=BytesIO(img_or_none),
            attachment_filename="cat.jpg",
            mimetype="image/jpeg"
        )

    return jsonify({
        "error": "this file is not image file."
    }), 500
