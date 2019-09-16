from flask import Flask

from services.data_service import DataService

app = Flask(__name__)


@app.route('/')
def hello_world():
    data_service = DataService()
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
