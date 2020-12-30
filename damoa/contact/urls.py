from django.urls import path
from . import views
 
urlpatterns = [
    path('listmessage/', views.listMessage, name='listMessage'),
    path('viewmessage/<int:id>/', views.viewMessage, name='viewMessage'),
    path('send', views.sendMessage, name='sendMessage'),
]
