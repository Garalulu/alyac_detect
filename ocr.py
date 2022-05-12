import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import easyocr
import numpy as np
import pandas as pd
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

class getTextfromImg:
    """
    getTextfromImg
    검색된 알약 리스트 리턴(JSON)하는 클래스
    __init__ 
        - file : 검색할 이미지명
        - ratio : 원본 이미지 비율
        - df : 낱알식별정보 csv
    """
    def __init__(self, file, ratio):
        # csv 파일 저장
        self.file = file
        self.df = pd.read_csv('OpenData_PotOpenTabletIdntfcC20220324.csv', dtype= {'표시앞':'object', '표시뒤':'object', '표기내용앞':'object', '표기내용뒤':'object'}, usecols=[0, 6, 7, 22, 23])
        self.df = self.df.fillna('-')
        self.ratio = ratio
    
    def getAlyac(self):
        # file 텍스트 검출
        reader = easyocr.Reader(['en'], gpu=True)
        result = reader.readtext(self.file)
        
        Alyaclist = self.searchText(result)
        
        return Alyaclist
        
    def searchText(self, txt):
        # 검색 실패 단어 저장용
        failed_list = []
        
        # position 추출
        # ratio를 곱해 원본 이미지 좌표 반환
        position = []
        for i in txt:
            x = int(i[0][0][0] * self.ratio)
            y = int(i[0][0][1] * self.ratio)
            w = int((i[0][1][0] - i[0][0][0]) * self.ratio)
            h = int((i[0][2][1] - i[0][1][1]) * self.ratio)
            position.append([x,y,w,h])
        
        # 표기내용 검색을 위한 검출 결과 전처리
        text = np.array(txt, dtype=object)
        text = np.delete(text, 0, 1)
        # dict 저장용
        result_list = dict()
        
        for i in range(0, len(text)):
            a = text[i][0].replace(" ", "")
            chklist = self.createList(a)
           
            # 한 단어 사이클마다 별개의 key 값으로 정리   
            if(len(chklist) != 0):
                temp_result = chklist.to_dict()
                
                # 단어 position 추가
                temp_result['position'] = position[i]
                result_list[i] = temp_result 
            else:
                # 검색 실패한 단어 추가
                failed_list.append([text[i][0].replace(" ", ""), i])
                
        while(failed_list):
            print("a={} 위치에 있는 값(b={}) 에 해당하는 알약이 없습니다. 글자를 직접 입력해주세요. (x키 입력으로 스킵)".format(position[failed_list[0][1]], failed_list[0][0])) 
            confirm = input(">> ")
            if(confirm != ("x" or "X")):
                chklist = self.createList(confirm)
                if(len(chklist) != 0):
                    temp_result = chklist.to_dict()
                
                    # 단어 position 추가
                    temp_result['position'] = position[i]
                    result_list[i] = temp_result 
                else:
                    print("해당하는 알약이 없습니다.") 
                    
            failed_list.pop(0)
        
        # 검색된 알약 0개
        if not result_list:
            return "해당하는 알약을 찾을 수 없습니다."        
        else:
            # Dict to JSON
            result_json = json.dumps(result_list, ensure_ascii=False, cls=NpEncoder)
            print(json.dumps(result_list, ensure_ascii=False, indent=4, cls=NpEncoder))                             
            return result_json
    
    def createList(self, text):
        # 빈 dataframe 생성
        chklist = pd.DataFrame(index=range(0,0), columns=['품목일련번호','표시앞','표시뒤','표기내용앞','표기내용뒤'])

        # 표시일부터 차례대로 검색
        chk = self.df.loc[self.df['표시앞'] == text] 
        if(len(chk) != 0):
            chklist = pd.concat([chklist,chk], ignore_index=True)
                
        chk = self.df.loc[self.df['표시뒤'] == text]
        if(len(chk) != 0):  
            chklist = pd.concat([chklist,chk], ignore_index=True)
                
        chk = self.df[self.df['표기내용앞'].str.contains(text)]
        if(len(chk) != 0):
            chklist = pd.concat([chklist,chk], ignore_index=True)
                
        chk = self.df[self.df['표기내용뒤'].str.contains(text)]
        if(len(chk) != 0):
            chklist = pd.concat([chklist,chk], ignore_index=True)
            
        return chklist