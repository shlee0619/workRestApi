import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import pandas as pd
import os

def getRequestURL(url, enc='utf-8'):
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            print(f"[{url}] 요청 성공")
            ret = response.read().decode(enc)
            return ret
        else:
            print("Error Code:", response.getcode())
            return None
    except Exception as e:
        print(f"요청 중 오류 발생: {e}")
        return None
def getNotificationData(serviceKey, numOfRows, pageNo):
    print('병무청 통지서 배달 결과 조회 getNotificationData()')
    url = 'http://apis.data.go.kr/1300000/tjsBdgg/list'
    parameters = {
        'serviceKey': serviceKey,
        'numOfRows': numOfRows,
        'pageNo': pageNo
    }
    encoded_params = urllib.parse.urlencode(parameters, safe="%")
    full_url = f"{url}?{encoded_params}"
    print(full_url)
    print()
    ret_data = getRequestURL(full_url)
    return ret_data
# 서비스 키 설정
serviceKey = '실제 서비스 키'

# 결과를 저장할 리스트 초기화
result = []

# 첫 페이지 데이터 가져오기
xml_data = getNotificationData(serviceKey, '10', '1')

if xml_data:
    root = ET.fromstring(xml_data)
    resultCode_element = root.find('.//resultCode')
    if resultCode_element is not None and resultCode_element.text == '00':
        totalCount_element = root.find('.//totalCount')
        numOfRows_element = root.find('.//numOfRows')
        if totalCount_element is not None and numOfRows_element is not None:
            totalCount = int(totalCount_element.text)
            numOfRows = int(numOfRows_element.text)
            # totalPages = (totalCount - 1) // numOfRows + 1  # 전체 페이지를 원하는 경우.

            for page in range(1, 10):
                xml_data = getNotificationData(serviceKey, str(numOfRows), str(page))
                if xml_data:
                    root = ET.fromstring(xml_data)
                    items = root.findall('.//item')
                    for item in items:
                        # 필요한 데이터 추출
                        bdgg = item.find('bdgg').text if item.find('bdgg') is not None else ''
                        bdymd = item.find('bdymd').text if item.find('bdymd') is not None else ''
                        bssy = item.find('bssy').text if item.find('bssy') is not None else ''
                        deunggiNo = item.find('deunggiNo').text if item.find('deunggiNo') is not None else ''
                        gwangye = item.find('gwangye').text if item.find('gwangye') is not None else ''
                        jsymd = item.find('jsymd').text if item.find('jsymd') is not None else ''
                        # 결과 리스트에 추가
                        result.append([bdgg, bdymd, bssy, deunggiNo, gwangye, jsymd])
                else:
                    print(f"{page} 페이지 데이터를 가져오지 못했습니다.")
        else:
            print("totalCount 또는 numOfRows를 찾을 수 없습니다.")
    else:
        resultMsg_element = root.find('.//resultMsg')
        if resultMsg_element is not None:
            print("API 호출 오류:", resultMsg_element.text)
        else:
            print("resultMsg 태그를 찾을 수 없습니다.")
else:
    print("데이터를 가져오지 못했습니다.")

print()
print(result)

# 데이터프레임 생성 및 CSV 저장
if result:
    df = pd.DataFrame(result, columns=['bdgg', 'bdymd', 'bssy', 'deunggiNo', 'gwangye', 'jsymd'])
    path = './data/NotificationData.csv'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, encoding='utf-8-sig', index=False)
    print(f"{path} 파일 저장 성공했습니다")
else:
    print("수집된 데이터가 없습니다.")
