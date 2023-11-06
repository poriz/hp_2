from django.shortcuts import render
from .models import AREA_INFO

# Create your views here.
def index(request):
    msg = '테스트 메세지'
    return render(request,'main/index.html',{'message':msg})

def data_to_db(request):
    # API에서 데이터 가져오기
    # data 에 API에서 딕셔너리화한 데이터를 반환
    # API 가져오는 함수 붙여넣으면 될 것 같습니다!
    datas = {}

    # 데이터베이스에 저장
    for data in datas:
        area_info = AREA_INFO(**data)
        area_info.save()

    return HttpResponse("Data saved")