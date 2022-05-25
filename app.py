import os
from re import I
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from flask import Flask, request
from flask_restx import Api, Resource  
from ocr import getTextfromImg
from todo import Alyac

from image_quality import change_img_quality
from image_crop import image_crop
import asyncio

from io import StringIO

# list to str
def return_print(*message):
    io = StringIO()
    print(*message, file=io, end="")
    return io.getvalue()

app = Flask(__name__)
api = Api(app)

api.add_namespace(Alyac, '/alyac')

result_file = 'images/image.jpg'

async def detect():
    # image.jpg가 있는지 확인
    while(not (os.path.isfile(result_file))):
        continue
    ratio = change_img_quality(result_file, 'images')
    position, folder = image_crop(r'images\image.jpg', ratio)
    alyac = getTextfromImg(folder, position)
    alyac_list = alyac.getAlyac()
    
    return alyac_list

async def check_file():
    # 출력 결과 텍스트로 저장
    alyac_list = await detect() 
    print(alyac_list)
    with open(r"result\result.txt", 'w') as file:
        file.write(return_print(alyac_list))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080) 
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_file())
    loop.close()    