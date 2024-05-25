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
from inmofacil_app.views import index, registro_inmueble, busqueda_inmueble, inmuebles_disponibles

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name='index'),
    path("registro_inmueble", registro_inmueble, name='registro_inmueble'),
    path("busqueda_inmueble", busqueda_inmueble, name='busqueda_inmueble'),
    path("inmuebles_disponibles", inmuebles_disponibles, name='inmuebles_disponibles'),
    
]