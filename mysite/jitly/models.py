from django.db import models

from django.db import models
class Link(models.Model): 
    # 슈퍼클래스 models의 하위클래스 Model을 상속받는다.
    # 필요한 데이터 정의
    
    original = models.TextField(null=False)
    encoded = models.CharField(max_length=8)

    def __str__(self):
        return self.original


# Create your models here.
