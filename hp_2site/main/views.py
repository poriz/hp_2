from dotenv import load_dotenv
import os

from django.shortcuts import render
from django.shortcuts import get_object_or_404,redirect
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from .models import *

# Open API와 크롤링을 위한 라이브러리
import requests
import xml.etree.ElementTree as ET

# schedule code
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()

import pandas as pd

# read env
load_dotenv(verbose=True)
APIKEY = os.getenv('api-key')

# Create your views here.
def index(request):
    # random을 추가해서 변경 가능합니다.
    crowded = AREA_INFO.objects.filter(AREA_CONGEST_LVL__in=['붐빔', '약간 붐빔']).order_by('AREA_CONGEST_LVL')[:3]
    uncrowded = AREA_INFO.objects.filter(AREA_CONGEST_LVL__in=['보통', '여유']).order_by('AREA_CONGEST_LVL')[:3]
    latest_comment = COMMENT.objects.order_by('-PUB_DATE')[:3]
    
    context = {'CROWDED' : crowded, 'UNCROWDED' : uncrowded, 'COMMENT' : latest_comment}
    return render(request,'main/index.html',context)

# API에서 최신 데이터 가져오기 (서울시 OpenAPI 서버상태에 따라 최장 시간 4~5분 소요)
@sched.scheduled_job('cron', minute ='*/5',name = 'schedulerName')
def data_to_db():
    current_time = timezone.now()
    print(f'cron start : {current_time}')
    currentPath = os.getcwd()
    # 이부분 DB에서 가져오는 방식도 좋습니다. pandas 에러로 파일 위치변경
    data = pd.read_csv(f'{currentPath}\\main\\place_name.CSV',encoding='utf-8')
    place_list = data['AREA_NM'].to_list()
    
    datas = list()
    columns = ['AREA_CD', 'AREA_NM', 'AREA_CONGEST_LVL', 'SKY_STTS', 'TEMP', 'PM10', 'PM25','TIMESTAMP']
    for place in place_list:
        url1 = f'http://openapi.seoul.go.kr:8088/{APIKEY}/xml/citydata/1/1/{place}'
        
        try:
            res = requests.get(url1)
        except:
            return print('request_error')
            
        root = ET.fromstring(res.text)
        
        c_dict = dict()
        for cl in columns:
            if cl == 'TIMESTAMP':
                c_dict[cl] = current_time
            else:
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
    # return render(request,'main/news.html', {'datas':datas})
    print('cron_fin')
sched.start()


def comment_write(request):
    errors = []
    if request.method == 'POST':
        name = request.POST.get('nickname','')
        content = request.POST.get('comment','')

        if not name :
            name = '익명'
        if not content :
            errors.append("댓글을 입력하세요.")
        if not errors :
            comment = COMMENT.objects.create(NICKNAME = name, COMMENT_TEXT = content)
            return redirect('main:index')
    return render(request,'index.html',{'name':name})

