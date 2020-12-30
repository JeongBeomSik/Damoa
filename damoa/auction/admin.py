from django.contrib import admin
from .models import Write, Bid, Rating
# Register your models here.

admin.site.register(Write)
admin.site.register(Bid)

admin.site.register(Rating) # 추가