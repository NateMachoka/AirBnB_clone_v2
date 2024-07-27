#!/usr/bin/python3

"""
Flask web application that listens on 0.0.0.0, port 5000.
Routes:
/ - displays "Hello HBNB!"
/hbnb - displays "HBNB"
/c/<text> - displays "C " followed by the value of the text variable
(replace underscore _ symbols with a space)
/python/<text> - displays "Python " followed by the value of the text variable
(replace underscore _ symbols with a space, default is "is cool")
"""

from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displaya 'HBNB'"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Displays 'C ' followed by the value of the text variable"""
    sanitized_text = escape(text.replace('_', ' '))
    return "C {}".format(sanitized_text)


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """Displays 'Python ' followed by the value of the text variable"""
    sanitized_text = escape(text.replace('_', ' '))
    return "Python {}".format(sanitized_text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
