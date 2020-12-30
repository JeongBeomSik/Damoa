from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name="member"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('findid/', views.findid, name="findid"),
    path('findpw/', views.findpw, name="findpw"),
]
