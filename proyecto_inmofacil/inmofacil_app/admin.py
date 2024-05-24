from django.contrib import admin
from .models import Region, Comuna, Direccion, Usuario, Inmueble

# Register your models here.
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Direccion)
admin.site.register(Usuario)
admin.site.register(Inmueble)

