from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroInmuebleForm, BusquedaInmuebleForm
from .models import Inmueble

# Create your views here.

def index(request):
    return render(request, 'index.html')


def registro_inmueble(request):
    if request.method == 'POST':
        form = RegistroInmuebleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inmueble_list')  # Redirige a la lista de inmuebles después de guardar
    else:
        form = RegistroInmuebleForm()
    return render(request, 'registro_inmueble.html', {'form': form})

def busqueda_inmueble(request):
    if request.method == 'POST':
        form = BusquedaInmuebleForm(request.POST)
        if form.is_valid():
            inmuebles = Inmueble.objects.all()
            if form.cleaned_data['region']:
                inmuebles = inmuebles.filter(direccion__comuna__region=form.cleaned_data['region'])
            if form.cleaned_data['comuna']:
                inmuebles = inmuebles.filter(direccion__comuna=form.cleaned_data['comuna'])
            if form.cleaned_data['tipo_inmueble']:
                inmuebles = inmuebles.filter(tipo_inmueble=form.cleaned_data['tipo_inmueble'])
            if form.cleaned_data['precio_max']:
                inmuebles = inmuebles.filter(valor_mensual__lte=form.cleaned_data['precio_max'])
            return render(request, 'resultados_busqueda.html', {'inmuebles': inmuebles})
    else:
        form = BusquedaInmuebleForm()
    return render(request, 'busqueda_inmueble.html', {'form': form})

def inmuebles_disponibles(request):
    inmuebles = Inmueble.objects.all()
    form = BusquedaInmuebleForm(request.GET or None)

    if form.is_valid():
        region = form.cleaned_data.get('region')
        comuna = form.cleaned_data.get('comuna')
        tipo_inmueble = form.cleaned_data.get('tipo_inmueble')
        precio_max = form.cleaned_data.get('precio_max')

        if region:
            inmuebles = inmuebles.filter(direccion_id__comuna_id__region_id=region)
        if comuna:
            inmuebles = inmuebles.filter(direccion_id__comuna_id=comuna)
        if tipo_inmueble:
            inmuebles = inmuebles.filter(tipo_inmueble=tipo_inmueble)
        if precio_max:
            inmuebles = inmuebles.filter(valor_mensual__lte=precio_max)

    context = {
        'form': form,
        'inmuebles': inmuebles
    }

    return render(request, 'inmuebles_disponibles.html', context)

def detalle_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, inmueble_id=inmueble_id)
    context = {
        'inmueble': inmueble
    }
    return render(request, 'detalle_inmueble.html', context)