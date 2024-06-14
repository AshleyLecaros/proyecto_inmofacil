from django import forms
from .models import Inmueble, Region, Comuna, Usuario, Direccion
from django.contrib.auth.hashers import make_password

# Clase para formulario de registro de inmueble 
class RegistroInmuebleForm(forms.ModelForm):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=True, label="Región")
    comuna_id = forms.ModelChoiceField(queryset=Comuna.objects.all(), required=True, label="Comuna")
    calle = forms.CharField(max_length=100, required=True, label="Calle")
    numero = forms.CharField(max_length=20, required=True, label="Número")
    departamento = forms.CharField(max_length=10, required=False, label="Departamento")

    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_contruidos', 'm2_terreno', 'cantidad_estacionamiento', 'cantidad_baños', 'tipo_inmueble', 'valor_mensual', 'foto_url' ]

    def save(self, commit=True):
        # Guardamos el inmueble sin commit para poder añadir la dirección y el propietario antes de guardarlo en l base de datos.
        inmueble = super().save(commit=False)

        # Creamos una nueva instancia de Dirección con los datos del formulario
        direccion = Direccion(
            calle=self.cleaned_data['calle'],
            numero=self.cleaned_data['numero'],
            departamento=self.cleaned_data.get('departamento', ''),
            comuna_id=self.cleaned_data['comuna_id']
        )
        # Guardamos la dirección en la base de datos
        direccion.save()

        # Asignamos la dirección al inmueble
        inmueble.direccion_id = direccion

        # Si commit es True, guardamos el inmueble en la base de datos
        if commit:
            inmueble.save()

        return inmueble
    
class BusquedaInmuebleForm(forms.Form):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=True, label="Región")
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), required=True, label="Comuna")
    tipo_inmueble = forms.ChoiceField(choices=Inmueble.tipo_inmueble_choice, required=False, label="Tipo de Inmueble")
    precio_max = forms.FloatField(required=False, label="Precio Máximo")

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')

    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellido', 'telefono', 'email', 'tipo_usuario', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.password = make_password(self.cleaned_data['password'])  # Usa make_password para encriptar la contraseña
        if commit:
            usuario.save()
        return usuario

# Formulario para editar los datos del usuario.
class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'rut', 'telefono', 'email', 'tipo_usuario']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
        

class EditarInmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_contruidos', 'm2_terreno', 'cantidad_estacionamiento', 'cantidad_baños', 'direccion_id', 'tipo_inmueble', 'valor_mensual', 'foto_url']

