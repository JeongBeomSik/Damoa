from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("mainsite.urls")),
    path('Login/', include('member.urls')),
    path('auction/', include("auction.urls")),
    path('mypage/', include("mypage.urls")),
    path('grouppurchase/', include("grouppurchase.urls")), # 수정
    path('contact/', include("contact.urls")), # 추가
    path('board/', include("board.urls")), # 추가
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
