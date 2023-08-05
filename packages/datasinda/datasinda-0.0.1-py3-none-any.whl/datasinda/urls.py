from django.contrib.auth.decorators import login_required
from django.urls import path, include 
from datasinda_backend import views 
 
urlpatterns = [ 
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/buscar/todas', views.buscar_todas),
    path('api/buscar/completas', views.buscar_todas_completas),
    path('api/buscar/sensores/<int:idPCD>', views.buscar_sensores),
    path('api/buscar/publicas', views.buscar_pcds_publicas),
    path('api/buscar/privadas', views.buscar_pcds_privadas),
    path('api/buscar/dados', views.buscar_dados),
    path('api/buscar/<int:idPCD>', views.buscar_pcd),
    path('api/buscar/<str:estado>', views.buscar_estado),
]