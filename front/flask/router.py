from flask import Flask
from .api_parameters import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World’

@app.route('/get_classif')
def get_classif() :

    """ this function process the classification of the query """

@app.route('/train_classif')
def train_classif() :

    """ this function process the training of the specified model """


if __name__ == '__main__':
    app.run(
        host = API_HOSTNAME,
        port = API_PORT,
        debug = API_RUN_MODE
    )