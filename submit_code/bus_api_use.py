import RPi.GPIO as GPIO
import time
import requests

# 여기에는 너가 핀 꽂는거에 따라 알아서 설정 ㄱㄱ
LED_PIN = 1
BUZZER_PIN = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

def alert_signal():
    GPIO.output(LED_PIN, GPIO.HIGH)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

def get_bus_location():
    api_key = ""    # 여기에 api 키 발급 받아서 입력하면 될듯?

    url = "http://apis.data.go.kr/1613000/BusLcInfoInqireService/getRouteAcctoBusLcList"
    params = {
        'serviceKey': api_key,
        
        # 여기도 알아서 채우셈
        'routeId': '',  # 버스 노선 ID
        'cityCode': '',  # 도시 코드
        
        'numOfRows': '10',
        'pageNo': '1',
        '_type': 'json'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['response']['header']['resultCode'] == '00':
            return data['response']['body']['items']['item']
        else:
            print("Error in API response")
    else:
        print(f"HTTP Error: {response.status_code}")
    return []

def is_bus_near(my_location, bus_locations):
    for bus in bus_locations:
        bus_location = (float(bus['gpsLati']), float(bus['gpsLong']))
        if abs(bus_location[0] - my_location[0]) < 0.001 and abs(bus_location[1] - my_location[1]) < 0.001:
            return True
    return False

my_location = ("위도", "경도")  # 너가 지정하고자 하는 위치? 도시?의 위도와 경도

try:
    while True:
        bus_locations = get_bus_location()
        if is_bus_near(my_location, bus_locations):
            alert_signal()
        time.sleep(30)  # 30초마다 확인
except KeyboardInterrupt:
    GPIO.cleanup()
