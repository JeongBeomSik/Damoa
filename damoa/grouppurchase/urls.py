from django.urls import path
from . import views

urlpatterns = [
    path('', views.gmain, name="gmain"),
    path('new/', views.gnew, name="gnew"),
    path('create/', views.gcreate, name="gcreate"),
    path('detail/<int:id>/', views.gdetail, name="gdetail"),
    path('updateordelete/<int:id>/', views.gupdateordelete, name="gupdateordelete"),
    path('update/<int:id>/', views.gupdate, name="gupdate"),
]

