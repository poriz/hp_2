from django.db import models

# Create your models here.
class AREA_INFO(models.Model):
    AREA_CD = models.CharField(max_length = 10, primary_key = True)
    AREA_NM = models.CharField(max_length = 255)
    AREA_CONGEST_LVL = models.CharField(max_length = 100)
    TEMP = models.FloatField()
    PM10 = models.FloatField()
    PM25 = models.FloatField()
    CATEGORY = models.CharField(max_length=50, default='분류오류')  # 카테고리 필드 추가
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
