import cv2, os
import numpy as np
from datetime import datetime

# Histogram equalization
def equalizeHist(img):
    img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

    img_ycrcb[:,:,0] = cv2.equalizeHist(img_ycrcb[:,:,0])
    dst = cv2.cvtColor(img_ycrcb, cv2.COLOR_YCrCb2BGR)
    
    return dst


def image_crop(original_image, ratio=1):
    """
    img_crop :: 이미지에서 알약 파트만 추출
    original_image : 원본 이미지
    ratio : 위치 비율
    """
    image = cv2.imread(original_image)
    dst = equalizeHist(image)
    image_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(image_gray, ksize=(3,3), sigmaX=0)

    edged = cv2.Canny(blur, 10, 250)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours_xy = np.array(contours, dtype=object)

    # x의 min과 max 찾기
    x_min, x_max = 0,0
    y_min, y_max = 0,0
    image_position = list()

    for i in range(len(contours_xy)):
        x_value = list()
        y_value = list()
        for j in range(len(contours_xy[i])):
            x_value.append(contours_xy[i][j][0][0]) 
            x_min = min(x_value)
            x_max = max(x_value)
            y_value.append(contours_xy[i][j][0][1])
            y_min = min(y_value)
            y_max = max(y_value)
        w = x_max - x_min
        h = y_max - y_min
        if(w >= 110 and h >= 40):
            image_position.append([x_min, y_min, x_max-x_min, y_max-y_min])

    img_path = 'cropped'
    count = 0
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    
    # 현재 시간으로 cropped 안에 폴더 생성
    now = datetime.now()
    folder = img_path + '/' + now.strftime('%Y%m%d%H%M%S')
    os.mkdir(folder)
    
    for i in image_position:
        filename = 'img_trim{}.jpg'.format(count)
        img_trim = image[i[1]:i[1]+i[3], i[0]:i[0]+i[2]]
        cv2.imwrite(os.path.join(folder, filename), img_trim)
        count += 1

    for j in range(len(image_position)):
        for k in range(len(image_position[j])):
            image_position[j][k] = int(image_position[j][k] * ratio)
            
    return image_position, folder