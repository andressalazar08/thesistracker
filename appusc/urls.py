from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import* 

urlpatterns=[
    path('', views.detail),
    path('welcome/',views.welcome),
    path('detail/',views.detail),
    path('register/',views.register),
    path('login/',views.login),
    path('dashboard/',views.dashboard,name='dash'),
    path('ctg_listaprofes_tm/',views.ctg_listaprofes_tm),
    path('ctg_listaestudiantes_tm/',views.ctg_listaestudiantes_tm),
    path('tragrados/',views.tragrados),
    path('nuevatutoria/',views.nuevatutoria),
    path('cargaarchivos/',views.cargaarchivos),
    path('tgrados_historial_tm/<int:pk>',views.tgrados_historial_tm,name='tgrados_historial_tm'),
    
]
# Esta se utiliza solo en desarrollo para que utilice la ruta de guardado de archivos de manera local
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)