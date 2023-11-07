from django.shortcuts import render
from .models import AREA_INFO

# Open API와 크롤링을 위한 라이브러리
import requests
import xml.etree.ElementTree as ET

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Create your views here.
def index(request):
    msg = '테스트 메세지'
    return render(request,'main/index.html',{'message':msg})

def news(request):
    place_list = list()
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get("https://data.seoul.go.kr/SeoulRtd/list")
        
        driver.implicitly_wait(3)
        
        for i in range(1, 10+1):
            place_list.append(driver.find_element(By.XPATH, f'//*[@id="srcd_list"]/a[{i}]/div/h4').text)

    apikey ='4b486663576c796837335278667276'

    p_dict = dict()
    for place in place_list:
        url1 = f'http://openapi.seoul.go.kr:8088/{apikey}/xml/citydata/1/1/{place}'
        
        res = requests.get(url1)
        root = ET.fromstring(res.text)
        
        columns = ['AREA_NM', 'AREA_CD', 'AREA_CONGEST_LVL', 'AREA_PPLTN_MIN', 'AREA_PPLTN_MAX', 'TEMP', 'SKY_STTS', 'PM10', 'PM25']
        
        c_dict = dict()
        
        for cl in columns:
            c_dict[cl] = root.find(f'.//{cl}').text
        
        p_dict[place] = c_dict
        
    return render(request,'main/news.html', {'p_dict':p_dict})

def data_to_db(request):
    # API에서 데이터 가져오기
    # data 에 API에서 딕셔너리화한 데이터를 반환
    # API 가져오는 함수 붙여넣으면 될 것 같습니다!
    datas = {}
    # git연습
    # 데이터베이스에 저장
    for data in datas:
        area_info = AREA_INFO(**data)
        area_info.save()

    return HttpResponse("Data saved")