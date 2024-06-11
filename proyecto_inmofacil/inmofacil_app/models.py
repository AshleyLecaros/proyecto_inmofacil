from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# Create your models here.
class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False, blank=False) 
    
    def __str__(self):
        return self.nombre
    
class Comuna(models.Model):
    comuna_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    region_id = models.ForeignKey('region', on_delete=models.CASCADE,related_name='comuna', null=False, blank=False)
    
    
    def __str__(self):
        return self.nombre
    
class Direccion(models.Model):
    direccion_id = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=100, null=False, blank=False)
    numero = models.CharField(max_length=20, null=False, blank=False)
    departamento = models.CharField(max_length=10)
    comuna_id = models.ForeignKey('comuna', on_delete=models.CASCADE,related_name='direccion', null=False, blank=False)
    
    
    def __str__(self):
        return f"{self.calle} {self.numero}, {self.comuna_id.nombre}"

# Gestor de usuarios personalizado

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, password=None):
        if not email:
            raise ValueError('El email debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre)
        user.set_password(password) # Hashea la contraseña
        user.save(using=self._db) # Guarda el usuario en la base de datos
        return user

    def create_superuser(self, email, nombre, password=None):
        user = self.create_user(email=email, nombre=nombre, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    rut = models.CharField(max_length=15, primary_key=True, null=False, blank=False)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    apellido = models.CharField(max_length=50, null=False, blank=False)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, null=False, blank=False, unique=True)
    tipo_de_usuario_choice = [
        ('arrendador', 'Arrendador'),
        ('arrendatario', 'Arrendatario'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices= tipo_de_usuario_choice, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'  # Usar el campo username para autenticación
    REQUIRED_FIELDS = ['nombre']

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
    
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.tipo_usuario})"


    
class Inmueble(models.Model):
    inmueble_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    descripcion = models.CharField(max_length=200, null=False, blank=False)
    m2_contruidos = models.CharField(max_length=20, null=False, blank=False)
    m2_terreno = models.CharField(max_length=20, null=False, blank=False)
    cantidad_estacionamiento = models.CharField(max_length=10, null=False, blank=False)
    cantidad_baños = models.CharField(max_length=10, null=False, blank=False)
    direccion_id = models.ForeignKey('direccion', on_delete=models.CASCADE,related_name='inmueble', null=False,          blank=False)
    tipo_inmueble_choice= [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('parcela','Parcela'),
    ] # choices es una lista de tuplas donde cada tupla contiene dos valores: el valor almacenado en la base de datos y la etiqueta legible que se mostrará en los formularios de Django.(define las opciones permitidas)
    tipo_inmueble = models.CharField(max_length=20, choices= tipo_inmueble_choice, null=False, blank=False)
    valor_mensual = models.FloatField(max_length=50, null=False, blank=False)
    foto_url = models.URLField()
    
    def __str__(self):
        return self.nombre