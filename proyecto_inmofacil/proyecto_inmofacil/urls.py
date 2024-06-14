"""
URL configuration for proyecto_inmofacil project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from inmofacil_app.views import index, registro_inmueble, inmuebles_disponibles, detalle_inmueble, registro_usuario, registro_exitoso, perfil, editar_perfil, mis_inmuebles, editar_inmueble

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name='index'),
    path("registro_inmueble", registro_inmueble, name='registro_inmueble'),
    path("inmuebles_disponibles", inmuebles_disponibles, name='inmuebles_disponibles'),
    path('inmuebles/<int:inmueble_id>/', detalle_inmueble, name='detalle_inmueble'),
    path('registro_usuario/', registro_usuario, name='registro_usuario'),
    path('registro_exitoso', registro_exitoso, name='registro_exitoso'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('perfil/', perfil, name='perfil'),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('mis_inmuebles/', mis_inmuebles, name='mis_inmuebles'),
    path('inmueble/<int:inmueble_id>/editar/', editar_inmueble, name='editar_inmueble'),
  
]
