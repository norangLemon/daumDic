from daumDic import *

l = ["사전", "사전 샤샤", '사전 .', '영어 안녕']#'국어 하늘', '영어 안녕','사전 a', '영어 ㅁ', '영어 hi', '국어 hi', '사전 ellop', '사전', '사전 뫄 뽷', '일어 곰']

for a in l:
    ho = daumDic(a)
    print(a+">>\t\t"+ho.getResult())
