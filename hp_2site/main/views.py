from dotenv import load_dotenv
import os

from django.shortcuts import render
from .models import AREA_INFO
from django.http import HttpResponse
from .models import *

# Open API와 크롤링을 위한 라이브러리
import requests
import xml.etree.ElementTree as ET

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

# read env
load_dotenv(verbose=True)
APIKEY = os.getenv('api-key')

# Create your views here.
def index(request):
    # random을 추가해서 변경 가능합니다.
    latest_AREA_INFO_list = AREA_INFO.objects.order_by('AREA_CONGEST_LVL')[:5]
    context = {'AREA_INFO' : latest_AREA_INFO_list}
    return render(request,'main/index.html',context)

# API에서 최신 데이터 가져오기 (서울시 OpenAPI 서버상태에 따라 최장 시간 4~5분 소요)
def data_to_db(request):
    data = pd.read_csv('./hp_2site/main/assets/place_name.csv',encoding='utf-8')
    place_list = data['AREA_NM'].to_list()
    
    datas = list()
    columns = ['AREA_CD', 'AREA_NM', 'AREA_CONGEST_LVL', 'SKY_STTS', 'TEMP', 'PM10', 'PM25']
    for place in place_list:
        url1 = f'http://openapi.seoul.go.kr:8088/{APIKEY}/xml/citydata/1/1/{place}'
        
        res = requests.get(url1)
        root = ET.fromstring(res.text)
        
        c_dict = dict()
        for cl in columns:
            tmp = root.find(f'.//{cl}').text
            if tmp:
                c_dict[cl] = root.find(f'.//{cl}').text
            else:
                c_dict[cl] = ""
        
        datas.append(c_dict)
    
    # 데이터베이스에 저장
    for data in datas:
        area_info = AREA_INFO(**data)
        area_info.save()

    return render(request,'main/news.html', {'datas':datas})