import urllib.request
# import urllib.request as req
import os.path
import json
import time



url = "https://api.github.com/repositories"
savename = "./data/test.json"
if not os.path.exists(savename):
    urllib.request.urlretrieve(url, savename)

print(savename, '파일저장 성공했습니다')
print()

print('./data/test.json 데이터읽어오기')
time.sleep(1)
items = json.load(open(savename, "r", encoding="utf-8"))
print(items)

#성공 path = open(savename, "r", encoding="utf-8").read()
#성공 mydata = json.loads(path)
# print(mydata)


print('- ' * 70)
for item in items:
    print(item["name"] + " : " + item["owner"]["login"])



print()
'''
json 파일 형식(2가지)  
 1. 중괄호 : dict 형식 문자열, 순서없음 
    예) {key : value} - usagov_bitly.txt
    json.loads() : dict 형식 문자열 -> python dict 

 2. 대괄호 : list형식 문자열, 순서있음 
    예) [{key : value}, {key : value}] - labels.json
    json.load() : list 형식 문자열 -> python list 
'''