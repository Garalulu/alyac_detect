import os

from requests import Response
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from flask import request
from flask_restx import Resource, Api, Namespace
import numpy as np
from ocr import getTextfromImg
from image_quality import change_img_quality
from PIL import Image

Alyac = Namespace('Alyac')

@Alyac.route('/upload')
class getFile(Resource):
    def get(self): 
        # pic_data = request.files['file'] # 서버에서 file을 받아서 사용해야 함. 현재 임시로 이미지 하나 설정해 구현
        ratio = change_img_quality('image.jpg', 'images')
        alyac = getTextfromImg(r'images\image.jpg', ratio)
        alyac_list = alyac.getAlyac()
        return alyac_list

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
        