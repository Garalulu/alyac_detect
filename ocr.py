import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import easyocr
import numpy as np
import pandas as pd

class getTextfromImg:
 
    def __init__(self, file):
        # csv 파일 저장
        self.file = file
        self.df = pd.read_csv('OpenData_PotOpenTabletIdntfcC20220324.csv', dtype= {'표시앞':'object', '표시뒤':'object', '표기내용앞':'object', '표기내용뒤':'object'}, usecols=[0, 6, 7, 22, 23])
        self.df = self.df.fillna('-')
    
    def getAlyac(self):
        # file 텍스트 검출
        reader = easyocr.Reader(['en'], gpu=True)
        result = reader.readtext(self.file)
        
        Alyaclist = self.searchText(result)
        
        return Alyaclist
        
    def searchText(self, txt):
        # position 추출
        position = []
        for i in txt:
            x = i[0][0][0]
            y = i[0][0][1]
            w = i[0][1][0] - i[0][0][0]
            h = i[0][2][1] - i[0][1][1]
            position.append([x,y,w,h])
        
        # 표기내용 검색을 위한 검출 결과 전처리
        text = np.array(txt, dtype=object)
        text = np.delete(text, 0, 1)
        # dict 저장용
        result_list = dict()
        
        for i in range(0, len(text)):
            # 빈 dataframe 생성
            chklist = pd.DataFrame(index=range(0,0), columns=['품목일련번호','표시앞','표시뒤','표기내용앞','표기내용뒤'])
            a = text[i][0].replace(" ", "")
            
            # 표시일부터 차례대로 검색
            chk = self.df.loc[self.df['표시앞'] == a] 
            if(len(chk) != 0):
                chklist = chklist.append(chk, ignore_index=True)
                
            chk = self.df.loc[self.df['표시뒤'] == a]
            if(len(chk) != 0):  
                chklist = chklist.append(chk, ignore_index=True)
                
            chk = self.df[self.df['표기내용앞'].str.contains(a)]
            if(len(chk) != 0):
                chklist = chklist.append(chk, ignore_index=True)
                
            chk = self.df[self.df['표기내용뒤'].str.contains(a)]
            if(len(chk) != 0):
                chklist = chklist.append(chk, ignore_index=True)
            
            # 한 단어 사이클마다 별개의 key 값으로 정리   
            if(len(chklist) != 0):
                temp_result = chklist.to_dict()
                
                # 단어 position 추가
                temp_result['position'] = position[i]
                result_list[i] = temp_result 
                
        return result_list
    
    