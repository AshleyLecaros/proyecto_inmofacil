from django import forms
from .models import Inmueble, Region, Comuna, Usuario, Direccion
from django.contrib.auth.hashers import make_password

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

# Formulario para editar los datos del usuario, incluyendo la dirección.
class EditarUsuarioForm(forms.ModelForm):
    calle = forms.CharField(max_length=100, required=True)
    numero = forms.CharField(max_length=20, required=True)
    departamento = forms.CharField(max_length=10, required=False)
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), required=True)

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'telefono', 'email', 'tipo_usuario']

    # Inicializa el formulario con los datos actuales del usuario y su dirección.
    def __init__(self, *args, **kwargs):
        super(EditarUsuarioForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.direccion_id:
            self.fields['calle'].initial = self.instance.direccion_id.calle
            self.fields['numero'].initial = self.instance.direccion_id.numero
            self.fields['departamento'].initial = self.instance.direccion_id.departamento
            self.fields['comuna'].initial = self.instance.direccion_id.comuna_id

    # Guarda los datos del formulario, actualizando o creando la dirección según sea necesario.
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            if not user.direccion_id:
                direccion = Direccion()
            else:
                direccion = user.direccion_id

            direccion.calle = self.cleaned_data['calle']
            direccion.numero = self.cleaned_data['numero']
            direccion.departamento = self.cleaned_data.get('departamento', '')
            direccion.comuna_id = self.cleaned_data['comuna']
            direccion.save()
            user.direccion_id = direccion
            user.save()
        return user

class EditarInmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_contruidos', 'm2_terreno', 'cantidad_estacionamiento', 'cantidad_baños', 'direccion_id', 'tipo_inmueble', 'valor_mensual', 'foto_url']

