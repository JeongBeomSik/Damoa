from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('new/', views.new, name='new'), # 상품 등록
    path('create/', views.create, name='create'), # 상품 등록
    path('', views.mainA, name='mainA'), # 등록된 게시글
    path('delete/', views.delete, name='delete'), # 임시
    path('detail/<int:id>/', views.detail, name='detail'), # 상품 상세
    #path('ajax/dataon/<int:id>', views.dataon, name="dataon")
    path('bidding/<int:id>', views.bidding, name='bidding'),
    path('fastpurchase/<int:id>', views.fastpurchase, name='fastpurchase'),
    path('writerinfo/<int:id>', views.writerinfo, name="writerinfo"),
    path('updateordelete/<int:id>/', views.updateordelete, name="updateordelete"), # 추가
    path('update/<int:id>/', views.update, name="update"), # 추가
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
