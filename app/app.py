#!/usr/bin/env python3
"""Initialize and configure flask instance of the app"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route("/", strict_slashes=False)
def home_page():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
