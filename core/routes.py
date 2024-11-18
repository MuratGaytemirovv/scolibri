from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from core import app

from core.db import (
    get_posts,
    add_post,
    get_post,
    delete_post,
    change_post,
    add_comment,
    delete_comment,
    change_comment,
)

upload_folder = os.path.join("static", "uploads")


app.config["UPLOAD"] = "core/static/uploads"


@app.route("/", methods=["GET", "POST"])
def index():
    search = request.args.get("search")
    posts = get_posts(search=search)
    return render_template("index.html", posts=posts)


def upload_file():
    file = request.files["img"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD"], filename))
    return filename


@app.route("/add_posts", methods=["GET", "POST"])
def add_post_fr():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        date_post = datetime.today()
        image = upload_file()

        add_post(
            title,
            description,
            date_post,
            image,
        )
        return redirect("/")
    return render_template("add_post.html")


@app.route("/posts/<int:id>")
def post_detail(id):
    post = get_post(id)
    return render_template("post_detail.html", post=post)


@app.route("/delete_post/<int:id>")
def delete_post_front(id):
    delete_post(id)
    return redirect("/")


@app.route("/delete_comment/<string:comment>/<int:id>")
def delete_comment_front(comment, id):
    delete_comment(comment, id)
    return redirect(url_for("post_detail", id=id))


@app.route("/change_comment/<string:comment>/<int:id>", methods=["GET", "POST"])
def change_comment_front(comment, id):
    if request.method == "POST":
        new_comment = request.form.get("new_comment")
        print(id, comment, new_comment)
        change_comment(comment, new_comment, id)
        return redirect(url_for("post_detail", id=id))
    return render_template("change_comment.html")


@app.route("/change_post", methods=["GET", "POST"])
def change_post_front():
    if request.method == "POST":
        id = request.args.get("id")
        title = request.form.get("title")
        description = request.form.get("description")
        change_post(int(id), title, description)
        return redirect(url_for("post_detail", id=id))
    return render_template("change_post.html")


@app.route("/add_comment", methods=["GET", "POST"])
def add_comment_front():
    if request.method == "POST":
        id = request.args.get("id")
        comment = request.form.get("comment")
        add_comment(int(id), comment)
        return redirect(url_for("post_detail", id=id))
