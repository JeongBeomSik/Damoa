from django.db import models

class GroupPurchase(models.Model):
    id = models.CharField(max_length=10, primary_key=True) #title
    name= models.CharField(max_length=50)   #작상자
    content = models.CharField(max_length=50, null=True)   #내용
    lookup = models.IntegerField(default=0) #조회수

class Group(models.Model):
    writer = models.CharField(max_length=10) # 작성자
    title = models.CharField(max_length=30) # 상품명
    content = models.TextField(null=True) # 상세내용
    url = models.TextField() # 링크
    recruit = models.PositiveIntegerField(default=0) # 모집인원
    lookup = models.PositiveIntegerField(default=0, null=True) # 조회수

