from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import post_view, tutoria_detalle

urlpatterns=[
    path('', views.detail),
    path('welcome/',views.welcome),
    path('detail/',views.detail),
    path('register/',views.register),
    path('login/',views.login),
    path('salida/',views.salida),
    path('dashboard/',views.dashboard,name='dash'),
    path('dashboardcopy/',views.dashboardcopy),
    path('base/',views.base),
    path('listaprofes/',views.listaprofes),
    path('listaestudiantes/',views.listaestudiantes),
    path('tutoriastgs/',views.tutoriastgs),
    path('nuevatutoria/',views.nuevatutoria),
    path('formularios/',views.cargaarchivos),
    path('ultima/<int:pk>',views.ultima,name='ultima'),
    path('entrega/',post_view.as_view(),name='posteostgs'),
    path('detallestutorias/<int:pk>',tutoria_detalle.as_view(),name='detallestutorias'),


]
# Esta se utiliza solo en desarrollo para que utilice la ruta de guardado de archivos de manera local
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)