from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('new/', views.new, name='boardnew'), # 상품 등록
    path('create/', views.create, name='boardcreate'), # 상품 등록
    path('', views.main, name='boardmain'), # 등록된 게시글
    path('delete/<int:id>/', views.delete, name='boarddelete'), # 임시
    path('detail/<int:id>/', views.detail, name='boarddetail'), # 상품 상세
    path('edit/<int:id>/', views.edit, name='boardedit'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)