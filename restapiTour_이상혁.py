import pandas as pd
import numpy as np
import time

#새로운import
import urllib.request
import json





def getRequestURL(url, enc='utf-8'):
    try:
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            print(f"[{url}] 요청 성공")
            return response.read().decode(enc)
    except Exception as e:
        print(e)
        print(f"[{url}] 요청 실패")
        return None

# 2단계: 국가 방문자 수 데이터 요청 함수 구현
def getNatVisitor(yyyymm, nat_cd, ed_cd):
    serviceKey='servicekey'  # 서비스키 입력
    url = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
    parameter = f'?_type=json&serviceKey={serviceKey}'
    parameter += f'&YM={yyyymm}'
    parameter += f'&NAT_CD={nat_cd}'
    parameter += f'&ED_CD={ed_cd}'
    url = url + parameter
    print(url)
    print('-' * 70)
    ret_data = getRequestURL(url)
    if ret_data is None:
        return None
    else:
        return json.loads(ret_data)

# 3단계: 데이터 수집 및 저장
result = []

for year in range(2017, 2019):   # 년도
    for month in range(1, 13):   # 월
        yyyymm = '{0}{1:0>2}'.format(str(year), str(month))
        json_data = getNatVisitor(yyyymm, '275', 'E')  # 중국(275), 방한(E)
        if json_data and json_data['response']['header']['resultMsg'] == 'OK':
            if json_data['response']['body']['items'] == '':
                print(f"{year}년 {month}월 데이터가 없습니다.")
                continue
            item = json_data['response']['body']['items']['item']
            natKorNm = item['natKorNm']
            num = item['num']
            ed = item['ed']
            print(f"{year}년 {month}월 {natKorNm}({ed}) 방문자 수: {num}명")
            result.append([yyyymm, natKorNm, '275', num])
        else:
            print(f"{year}년 {month}월 데이터 수신 실패")

print()
print(result)

# 데이터프레임 생성 및 CSV 저장
df = pd.DataFrame(result, columns=['년월', '국가명', '국가코드', '방문자수'])
path = './data/tour.csv'
df.to_csv(path, encoding='cp949', index=False)
print(f"{path} 파일 저장 성공했습니다")
print('restAPI testing 완료')

