from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# 7.30 수정
class Profile(models.Model):
    email = models.CharField(max_length=30,blank=True)
    name = models.CharField(max_length=10) # 성함
    location = models.CharField(max_length=30, blank=True) # 집주소
    phonenumber = models.CharField(max_length=15,blank=True) # 전화번호
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True) # 판매자등록