#!/usr/bin/python3
"""
Flask web application that listens on 0.0.0.0, port 5000.
Routes:
- / - displays "Hello HBNB!"
- /hbnb - displays "HBNB"
- /c/<text> - displays "C " followed by the value of the text variable
(replacing underscore _ with a space)
- /python/(<text>) - displays "Python " followed by the value of the text
variable (replacing underscore _ with a space, default is "is cool")
- /number/<n> - displays "n is a number" only if n is an integer
- /number_template/<n> - displays a HTML page with H1 tag "Number: n"
if n is an integer
"""

from flask import Flask, render_template_string
from markupsafe import escape

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Displays 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays 'HBNB'"""
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


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """Displays 'n is a number' only if n is an integer"""
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Displays a HTML page with H1 tag 'Number: n' if n is an integer"""
    html_content = "<html><body><h1>Number: {}</h1></body></html>".format(n)
    return render_template_string(html_content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
