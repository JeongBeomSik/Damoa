from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import json
import ast
# Create your models here.

class Write(models.Model): # 상품 등록
    CATEGORY_CHOICES = (
        ('식품', '식품'),
        ('가구/생활/건강', '가구/생활/건강'),
        ('디지털/가전', '디지털/가전'),
        ('의류/잡화', '의류/잡화'),
        ('뷰티', '뷰티'),
        ('도서/취미/상품권', '도서/취미/상품권'),
        ('레저/자동차', '레저/자동차'),
        ('반려동물', '반려동물')
    ) # 0804 추가
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES,blank=True) # 0804 추가
    writer = models.CharField(max_length=10) # 작성자
    up_date = models.DateTimeField('date published', auto_now=True) # 작성시간
    title = models.CharField(max_length=30, null=False) # 상품명
    image = models.ImageField(upload_to='images/', null = True, blank=True) 
    content = models.TextField(null=True,blank=True) # 상세 내용
    buyitnow = models.PositiveIntegerField(default=0, null=False) # 즉시구매가
    up_price = models.PositiveIntegerField(default=0) # 시작가
    lookup = models.PositiveIntegerField(default=0) # 조회수
    e_date = models.DateTimeField('date published') # 종료일 !!! 새로 수정된 곳
    #biddings = models.ManyToManyField(settings.AUTH_USER_MODEL,through="Bid",through_fields=('writerId','userId'))
    biddings = models.CharField(max_length=200, default="{u'li':[]}")
    confirm = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    def set_biddings(self, x):
        x = json.dumps(x)
        print(x)
        x = x.replace('"',"'")
        print(x)
        x = x.replace("{'","{u'")
        self.biddings = x
        print(self.biddings)
    def get_biddings(self):
        self.biddings = self.biddings.replace("'",'"')
        return json.loads(self.biddings.replace('u"','"'))

class Bid(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    writerId = models.ForeignKey(Write,on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)

class Addsale(models.Model):
    salesperson = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

class Rating(models.Model): # 0804 추가
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True) # 판매자등록
    grade = models.CharField(max_length=1, null=True) # 평점
    comment = models.CharField(max_length=30, null=True) # 한줄평