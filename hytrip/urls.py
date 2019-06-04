from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls'), name='index'),
    path('maps/', include('maps.urls'), name='maps'),
    path('post/', include('post.urls'), name='post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# django.contrib.auth.urls -> 장고에 기본적으로 내장된 인증 기능.