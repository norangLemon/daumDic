import re
import requests
from bs4 import BeautifulSoup

# daum 어학사전을 검색
# http://dic.daum.net/

class daumDic():
    session = requests.Session()
    addr = "http://dic.daum.net/search.do?q="
    addr_re = "http://dic.daum.net/word/view.do?wordid="    # 리다이렉트 되는 경우가 있음
    map_dic = {     # 사전 조건 매핑
            "사전":"",
            "국어":"&dic=kor",
            "영어":"&dic=eng",
            "일어":"&dic=jp"
            }

    def __init__(self, string):
        # instance 변수 설정
        ## 검색 키워드
        self.word = None 
        self.dic = None
        ## BeautifulSoup 파싱: 검색 결과
        self.search_word = None
        self.search_list = None
        self.search_dic = None
        ## 출력할 검색 결과

        # 명령어 parsing
        parsed = string.split()

        if len(parsed) != 2:
            return
        
        self.dic = daumDic.map_dic.get(parsed[0])
        self.word = parsed[1]

        self.search()

    def search(self):
        if not self.word:
            return ""
        addr = daumDic.addr + self.word + self.dic
        
        daumDic.session.encoding = "utf-8"
        req = daumDic.session.get(addr)

        soup_raw = BeautifulSoup(req.text, "html.parser")
        self.search_dic = soup_raw.find(class_="ir_wa")
        if not self.search_dic:
            word_key = soup_raw.find(string = re.compile("kew\d{9}"))   # 정규식을 써서 단어의 번호를 찾아낸다
            if word_key:
                addr = daumDic.addr_re + word_key                       # redirect되는 주소를 알아낸다
                req = daumDic.session.get(addr)
                soup_raw = BeautifulSoup(req.text, "html.parser")
                self.search_dic = soup_raw.find(class_="ir_wa")

                if not self.search_dic:
                    return
                else:
                    return
        

        soup = soup_raw.find(class_="search_box")
        
        if not soup:
            # 페이지 형식이 다른 경우
            soup = soup_raw.find(class_="inner_top")

            # 검색 결과가 없는 경우
            if not soup:
                return
            self.search_word = soup.find(class_="txt_cleanword")
            self.search_list = soup.find(class_="list_mean").find_all(class_="txt_mean")
            
        else:    
            self.search_word = soup.find(class_= re.compile("_cleanword"))
            self.search_list = soup.find(class_="list_search").find_all(class_="txt_search")

    def getResult(self):
        if not self.search_list or not self.search_word:
            return "검색 결과가 존재하지 않습니다"
        result = '[' + self.search_dic.text + '] ' + self.search_word.find("span").text + ": "

        for mean in self.search_list:
            result += mean.text + ", "
        
        return result.strip(', ')
