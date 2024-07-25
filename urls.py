from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('setting/', views.setting, name='setting'),
    path('', views.home, name="home"),
    path('send_msg', views.send_msg, name="send_msg"),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
