from django.contrib import admin
from django.urls import path
from rag import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('setting/', views.setting, name='setting'),
    path('', views.home, name="home"),
    path('send_msg/', views.send_msg, name="send_msg"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)