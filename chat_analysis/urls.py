from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings



from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from chat_analysis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('process', views.process),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)