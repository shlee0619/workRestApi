import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import pandas as pd
import os

# 1단계: API 요청 함수 정의
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

# 2단계: 건축 인허가 정보 조회 함수 정의
def getArchitectureData(serviceKey, sigunguCd, bjdongCd, platGbCd, bun, ji, numOfRows, pageNo):
    print('국토교통부_건축인허가 기본개요 조회 getArchitectureData()')
    url = 'http://apis.data.go.kr/1613000/ArchPmsService_v2/getApBasisOulnInfo'
    parameters = {
        'serviceKey': serviceKey,
        'sigunguCd': sigunguCd,
        'bjdongCd': bjdongCd,
        'platGbCd': platGbCd,
        'bun': bun,
        'ji': ji,
        'numOfRows': numOfRows,
        'pageNo': pageNo
    }
    encoded_params = urllib.parse.urlencode(parameters, safe="%")
    full_url = f"{url}?{encoded_params}"
    print(full_url)
    print()
    ret_data = getRequestURL(full_url)
    return ret_data

# 3단계: 메인 실행 부분
serviceKey = '서비스 키로 실행'

# 결과를 저장할 리스트 초기화
result = []

# 첫 페이지 데이터 가져오기
xml_data = getArchitectureData(serviceKey, '11680', '10300', '0', '0012', '0004', '10', '1')

if xml_data:
    root = ET.fromstring(xml_data)
    resultCode_element = root.find('.//resultCode')
    if resultCode_element is not None and resultCode_element.text == '00':
        totalCount_element = root.find('.//totalCount')
        numOfRows_element = root.find('.//numOfRows')
        if totalCount_element is not None and numOfRows_element is not None:
            totalCount = int(totalCount_element.text)
            numOfRows = int(numOfRows_element.text)
            totalPages = (totalCount - 1) // numOfRows + 1  # 전체 페이지 수 계산

            for page in range(1, totalPages + 1):
                xml_data = getArchitectureData(serviceKey, '11680', '10300', '0', '0012', '0004', str(numOfRows), str(page))
                if xml_data:
                    root = ET.fromstring(xml_data)
                    items = root.findall('.//item')
                    for item in items:
                        # 필요한 데이터 추출
                        archArea = item.find('archArea').text if item.find('archArea') is not None else ''
                        archGbCdNm = item.find('archGbCdNm').text if item.find('archGbCdNm') is not None else ''
                        platPlc = item.find('platPlc').text if item.find('platPlc') is not None else ''
                        bldNm = item.find('bldNm').text if item.find('bldNm') is not None else ''
                        useAprDay = item.find('useAprDay').text if item.find('useAprDay') is not None else ''
                        # 결과 리스트에 추가
                        result.append([archArea, archGbCdNm, platPlc, bldNm, useAprDay])
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
    df = pd.DataFrame(result, columns=['archArea', 'archGbCdNm', 'platPlc', 'bldNm', 'useAprDay'])
    path = './data/ArchitectureData.csv'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, encoding='utf-8-sig', index=False)
    print(f"{path} 파일 저장 성공했습니다")
else:
    print("수집된 데이터가 없습니다.")
