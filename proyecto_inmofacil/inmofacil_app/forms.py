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

