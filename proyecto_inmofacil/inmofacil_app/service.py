from .models import Region, Comuna, Direccion, Usuario, Inmueble

# Funciones para crear un objeto con el modelo especificado
def crear_region(nombre):
    region = Region.objects.create(nombre=nombre)
    return region

def crear_comuna(nombre, region):
    comuna = Comuna.objects.create(nombre=nombre, region_id=region)
    return comuna

def crear_direccion(calle, numero, departamento, comuna):
    direccion = Direccion.objects.create(calle=calle, numero=numero, departamento=departamento, comuna_id=comuna)
    return direccion

def crear_usuario(rut, nombre, apellido, direccion, telefono, mail, tipo_usuario):
    usuario = Usuario.objects.create(
        rut=rut, 
        nombre=nombre, 
        apellido=apellido, 
        direccion_id=direccion, 
        telefono=telefono, 
        mail=mail, 
        tipo_usuario=tipo_usuario
    )
    return usuario

def crear_inmueble(nombre, descripcion, m2_contruidos, m2_terreno, cantidad_estacionamiento, cantidad_baños, direccion, tipo_inmueble, valor_mensual):
    inmueble = Inmueble.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        m2_contruidos=m2_contruidos,
        m2_terreno=m2_terreno,
        cantidad_estacionamiento=cantidad_estacionamiento,
        cantidad_baños=cantidad_baños,
        direccion_id=direccion,
        tipo_inmueble=tipo_inmueble,
        valor_mensual=valor_mensual
    )
    return inmueble

# Enlistar desde el modelo de datos
def listar_regiones():
    return Region.objects.all()

def listar_comunas():
    return Comuna.objects.all()

def listar_direcciones():
    return Direccion.objects.all()

def listar_usuarios():
    return Usuario.objects.all()

def listar_inmuebles():
    return Inmueble.objects.all()

# Actualizar un registro en el modelo de datos, el uso de **kwargs me permite poder actualizar uno o mas datos a la vez (los argumentos se agrupan en un diccionario dentro de la función, lo que te permite actualizar multiples campos de un modelo de Django en una sola llamada a la función.)
def actualizar_usuario(rut, **kwargs):
    Usuario.objects.filter(rut=rut).update(**kwargs)

def actualizar_inmueble(inmueble_id, **kwargs):
    Inmueble.objects.filter(inmueble_id=inmueble_id).update(**kwargs)

# Borrar un registro del modelo de datos
def borrar_usuario(rut):
    Usuario.objects.filter(rut=rut).delete()

def borrar_inmueble(inmueble_id):
    Inmueble.objects.filter(inmueble_id=inmueble_id).delete()
