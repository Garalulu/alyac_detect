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
        - folder : 검색할 이미지 위치
        - list : 검색할 이미지 리스트
        - position : 원본 이미지 좌표
        - df : 낱알식별정보 csv
    """
    def __init__(self, folder, position):
        # csv 파일 저장
        self.folder = folder
        self.list = os.listdir(folder)
        self.df = pd.read_csv('OpenData_PotOpenTabletIdntfcC20220324.csv', dtype= {'표시앞':'object', '표시뒤':'object', '표기내용앞':'object', '표기내용뒤':'object'}, usecols=[0, 6, 7, 22, 23])
        self.df = self.df.fillna('-')
        self.position = position
    
    def getAlyac(self):
        # file 텍스트 검출 
        Alyaclist = self.searchText(self.list)
        
        return Alyaclist
        
    def searchText(self, alist):
        test_list = []
        # 검색 실패 단어 저장용
        failed_list = []
        
        # dict 저장용
        result_list = dict()
        
        reader = easyocr.Reader(['en'], gpu=True)
        for i in range(len(alist)):
            result = reader.readtext(os.path.join(self.folder, alist[i]))
            # 표기내용 검색을 위한 검출 결과 전처리
            text = np.array(result, dtype=object)
            try:
                text = np.delete(text, 0, 1)
            except:
                # 검색된 알약 0개
                continue

            a = text[0][0].replace(" ", "")
            chklist = self.createList(a)
           
            # 한 단어 사이클마다 별개의 key 값으로 정리   
            if(len(chklist) != 0):
                temp_result = chklist.to_dict()
                
                # 단어 position 추가
                temp_result['position'] = self.position[i]
                result_list[i] = temp_result 
                
                test_list.append(list(temp_result['품목일련번호'].values()))
            else:
                # 검색 실패한 단어 추가
                failed_list.append([text[0][0].replace(" ", ""), i])
                   
        while(failed_list):
            print("a={} 위치에 있는 값(b={}) 에 해당하는 알약이 없거나 너무 많습니다. 글자를 다시 입력해주세요. (x키 입력으로 스킵)".format(self.position[failed_list[0][1]], failed_list[0][0])) 
            confirm = input(">> ")
            if(confirm != ("x" or "X")):
                chklist = self.createList(confirm)
                if(len(chklist) != 0):
                    temp_result = chklist.to_dict()
                
                    # 단어 position 추가
                    temp_result['position'] = self.position[failed_list[0][1]]
                    result_list[failed_list[0][1]] = temp_result 
                    
                    test_list.append(list(temp_result['품목일련번호'].values()))
                else:
                    print("해당하는 알약이 없습니다.") 
                    
            failed_list.pop(0)
        
        # Dict to JSON
        result_json = json.dumps(result_list, ensure_ascii=False, cls=NpEncoder)
        print(json.dumps(result_list, ensure_ascii=False, indent=4, cls=NpEncoder))                             
        # return result_json
        return test_list
    
    def createList(self, text):
        print(text)
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