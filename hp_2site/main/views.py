from django.shortcuts import render

# Create your views here.
def index(request):
    msg = '테스트 메세지'
    return render(request,'main/index.html',{'message':msg})