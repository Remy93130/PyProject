"""Entry point from the application
contains the different controller
and return data needed according to
the user request
"""

from flask import Flask, jsonify

from services.data_service import DataService

app = Flask(__name__)


@app.route('/')
def hello_world():
    """A beautiful hello world to test
    the program because you can't bypass it"""
    return jsonify({"message": "Hello World!"})


if __name__ == '__main__':
    app.run()
