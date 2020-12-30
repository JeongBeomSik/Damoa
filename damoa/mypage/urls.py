from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.mymain, name="mymain"),
    path('profileedit/<int:id>/', views.profileedit, name="proedit"), #0808 추가
]