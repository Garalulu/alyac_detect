import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from flask import Flask, request
from flask_restx import Api, Resource  
from ocr import getTextfromImg
from todo import Alyac

app = Flask(__name__)
api = Api(app)

api.add_namespace(Alyac, '/alyac')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080) 