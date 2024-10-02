import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_lat_lon(address):
    geolocator = Nominatim(user_agent="my_agent")
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except (GeocoderTimedOut, GeocoderServiceError):
        print("Error: 지오코딩 서비스에 문제가 발생했습니다. 다시 시도해주세요.")
        return None, None
# 주소 입력 받기 ~로 건물번호 형식 예) 서울 마포구 양화로 122
address = input("상세 주소를 입력하세요: ")
# 위도와 경도 얻기
lat, lon = get_lat_lon(address)
print(f"\n입력한 주소: {address}")
print(f"위도: {lat}")
print(f"경도: {lon}")