from importlib.resources import contents
import os

from requests import Response
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from flask import request
from flask_restx import Resource, Api, Namespace
import numpy as np
from ocr import getTextfromImg
import json

# dict to json 인코딩 구성
class NpEncoder(json.JSONEncoder): 
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

Alyac = Namespace('Alyac')

@Alyac.route('/upload')
class getFile(Resource):
    def get(self):
        pic_data = request.files['file'] # 서버에서 file을 받아서 사용해야 함. 현재 임시로 이미지 하나 설정해 구현
        alyac = getTextfromImg('ah8dexs6nd1y302.jpg')
        alyac_list = alyac.getAlyac()
        alyac_json = json.dumps(alyac_list, ensure_ascii=False, cls=NpEncoder) 
        return alyac_json


@Alyac.route('/<int:todo_id>')
class TodoSimple(Resource):
    def get(self, todo_id):
        return {
            'todo_id': todo_id,
        }

    def put(self, todo_id):
        return {
            'todo_id': todo_id,
        }
    
    def delete(self, todo_id):
        return {
            "delete" : "success"
        }
        