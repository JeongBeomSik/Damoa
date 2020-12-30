from django.db import models
# Create your models here.

class BoardWrite(models.Model): # 상품 등록
    writer = models.CharField(max_length=10) # 작성자
    up_date = models.DateTimeField('date published', auto_now=True) # 작성시간
    title = models.CharField(max_length=30, null=False) # 상품명
    image = models.ImageField(upload_to='images/', null = True, blank=True) 
    content = models.TextField(null=True,blank=True) # 상세 내용
    lookup = models.PositiveIntegerField(default=0) # 조회수
    