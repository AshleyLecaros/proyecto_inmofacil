from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroInmuebleForm, BusquedaInmuebleForm, RegistroUsuarioForm, EditarUsuarioForm, EditarInmuebleForm
from .models import Inmueble, Usuario, Direccion
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'index.html')


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

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro_exitoso')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registro_usuario.html', {'form': form})


def registro_exitoso(request):
    return render(request, 'registro_exitoso.html')


# Vista para ver el perfil del usuario.
@login_required
def perfil(request):
    usuario = get_object_or_404(Usuario, email=request.user.email)
    return render(request, 'perfil.html', {'usuario': usuario})

# Vista para editar el perfil del usuario.
@login_required
def editar_perfil(request):
    usuario = get_object_or_404(Usuario, email=request.user.email)
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = EditarUsuarioForm(instance=usuario)
    return render(request, 'editar_perfil.html', {'form': form})

# Vista para que el arrendador vea sus inmuebles.
@login_required
def mis_inmuebles(request):
    usuario = get_object_or_404(Usuario, email=request.user.email)
    if usuario.tipo_usuario != 'arrendador':
        return redirect('perfil')

    inmuebles = Inmueble.objects.filter(propietario=usuario)
    return render(request, 'mis_inmuebles.html', {'inmuebles': inmuebles})
# Vista para que el arrendador registre un nuevo inmueble.
@login_required
def registro_inmueble(request):
    usuario = get_object_or_404(Usuario, email=request.user.email)
    if usuario.tipo_usuario != 'arrendador':
        return redirect('perfil')

    if request.method == 'POST':
        form = RegistroInmuebleForm(request.POST)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.save()
            return redirect('mis_inmuebles')
    else:
        form = RegistroInmuebleForm()
    return render(request, 'registro_inmueble.html', {'form': form})

# Vista para editar un inmueble existente del arrendador.
@login_required
def editar_inmueble(request, inmueble_id):
    usuario = get_object_or_404(Usuario, email=request.user.email)
    if usuario.tipo_usuario != 'arrendador':
        return redirect('perfil')

    inmueble = get_object_or_404(Inmueble, inmueble_id=inmueble_id)
    if request.method == 'POST':
        form = EditarInmuebleForm(request.POST, instance=inmueble)
        if form.is_valid():
            form.save()
            return redirect('inmueble_detalle', inmueble_id=inmueble.inmueble_id)
    else:
        form = EditarInmuebleForm(instance=inmueble)
    return render(request, 'editar_inmueble.html', {'form': form})


