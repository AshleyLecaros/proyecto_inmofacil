from django import forms
from .models import Inmueble, Region, Comuna, Usuario, Direccion

# Clase para formulario de registro de inmueble 
class RegistroInmuebleForm(forms.ModelForm):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=True, label="Región")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), required=True, label="Comuna")
    calle = forms.CharField(max_length=100, required=True, label="Calle")
    numero = forms.CharField(max_length=20, required=True, label="Número")
    departamento = forms.CharField(max_length=10, required=False, label="Departamento")

    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_contruidos', 'm2_terreno', 'cantidad_estacionamiento', 'cantidad_baños', 'tipo_inmueble', 'valor_mensual']

    def save(self, commit=True):
        inmueble = super().save(commit=False)
        direccion = Direccion(
            calle=self.cleaned_data['calle'],
            numero=self.cleaned_data['numero'],
            departamento=self.cleaned_data.get('departamento', ''),
            comuna=self.cleaned_data['comuna']
        )
        direccion.save()
        inmueble.direccion = direccion
        if commit:
            inmueble.save()
        return inmueble
    
class BusquedaInmuebleForm(forms.Form):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=True, label="Región")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), required=True, label="Comuna")
    tipo_inmueble = forms.ChoiceField(choices=Inmueble.tipo_inmueble_choice, required=False, label="Tipo de Inmueble")
    precio_max = forms.FloatField(required=False, label="Precio Máximo")

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput) #para que el campo se renderice como un campo de entrada de contraseña en HTML, ocultando los caracteres ingresados.

    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'password'] #define una lista de campos del modelo que se incluirán en el formulario.

    def clean_email(self): # Aquí se verifica si ya existe un usuario con el mismo email en la base de datos
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email

    def save(self, commit=True):
        usuario = super().save(commit=False) #que crea una instancia del modelo Usuario, pero no la guarda en la base de datos aún.
        usuario.set_password(self.cleaned_data['password']) #toma la contraseña ingresada y la convierte en una cadena de caracteres (el hash) segura.
        if commit: #Si commit es True, se guarda finalmente la instancia en la base de datos.
            usuario.save()
        return usuario

