from django.db import models

# Create your models here.
class AREA_INFO(models.Model):
    AREA_CD = models.CharField(max_length = 10) # 프라이머리키 자동생성
    AREA_NM = models.CharField(max_length = 255)
    AREA_CONGEST_LVL = models.CharField(max_length = 100)
    SKY_STTS = models.CharField(max_length = 100, default='정보없음') # 프론트 설계 화면에 '맑음', '흐림'등이 있어 새 필드를 추가했습니다.
    TEMP = models.FloatField()
    PM10 = models.CharField(max_length = 50)
    PM25 = models.CharField(max_length = 50)
    CATEGORY = models.CharField(max_length = 50, default='분류오류')  # 카테고리 필드 추가

    def select_category(self):
        if int(self.AREA_CD[-3:]) >= 1 and int(self.AREA_CD[-3:]) <= 7:
            return '관광특구'
        
        elif int(self.AREA_CD[-3:]) >= 8 and int(self.AREA_CD[-3:]) <= 12:
            return '고궁·문화유산'
        
        elif int(self.AREA_CD[-3:]) >= 13 and int(self.AREA_CD[-3:]) <= 56:
            return '인구밀집지역'
        
        elif int(self.AREA_CD[-3:]) >= 57 and int(self.AREA_CD[-3:]) <= 84:
            return '발달상권'
        
        elif int(self.AREA_CD[-3:]) >= 85 and int(self.AREA_CD[-3:]) <= 113:
            return '공원'
        
        else:
            return '분류오류'
    def save(self, *args, **kwargs):
        self.CATEGORY = self.select_category()  # 카테고리를 설정
        super(AREA_INFO, self).save(*args, **kwargs)  # 부모 클래스의 save 메서드 호출
    
    def __str__(self):
        return f'{self.AREA_NM}, {self.CATEGORY}, {self.AREA_CONGEST_LVL}, {self.SKY_STTS}, {self.TEMP}, {self.PM10}, {self.PM25}'

class COMMENT(models.Model):
    NICKNAME = models.CharField(max_length=30)
    COMMENT_TEXT = models.CharField(max_length=400)
    PUB_DATE = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.COMMENT_TEXT
    


