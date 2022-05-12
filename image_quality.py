import os
import sys
from PIL import Image

def change_img_quality(original_image, change_path, quality=85):
    """
    change_img_quality :: 검색할 이미지를 새로운 경로에 저장하고, 리사이즈했을 경우 리사이즈 비율 반환
    original_image : 원본 이미지
    change_path : 변경 후 저장 경로
    quality : 품질
    """
    
    # 원본 : 리사이즈 비율
    ratio = 1
    
    if not os.path.exists(change_path):
        os.mkdir(change_path)
    try:
        img_path = os.path.dirname(os.path.abspath(original_image))
    except FileNotFoundError as e:
        print("이미지 원본 디렉터리가 존재하지 않습니다.")
        sys.exit(0)
    file = img_path + '\\' + original_image
    im = Image.open(file)
    img_width, img_height = im.size
    
    # 이미지 가로 사이즈가 1000 이상일 경우
    if(img_width >= 1000):
        # 이미지 리사이즈
        ratio = img_width / 1000
        resize_image = im.resize((1000, int(img_height / ratio)))
        resize_image.save('image-resized.jpg')
        file = img_path + '\\' + 'image-resized.jpg'
        im = Image.open(file)
    
    # change_path에 이미지 저장 (퀄리티 85)    
    im.save(os.path.join(change_path, original_image), quality = quality)

    # 이미지 원본 사이즈 ratio 리턴
    return ratio
