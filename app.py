import os
import openai
from flask import Flask, render_template, request
from prompt import use_thesaurus

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        word = request.form["word"]
        posts = use_thesaurus(word)

        return render_template("index.html", posts=posts, word=word)

    return render_template("index.html")
