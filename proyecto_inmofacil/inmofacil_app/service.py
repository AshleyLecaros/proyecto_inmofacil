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



# Función para listar inmuebles por comuna y guardar en un archivo de texto
def listar_inmuebles_por_comuna():
    # Realiza una consulta a la base de datos para obtener los campos 'nombre' y 'descripcion' del Inmueble, así como el nombre de la comuna relacionada.
    inmuebles = Inmueble.objects.values('nombre', 'descripcion', 'direccion_id__comuna_id__nombre') #doble guion bajo (__) permite acceder a campos del modelo relacionado. permite acceder al nombre de la comuna a través de la relación de la dirección del inmueble (Direccion tiene una clave foránea a Comuna).

    # Definimos la ruta del archivo donde guardaremos los resultados
    file_path = 'inmuebles_por_comuna.txt'
    
    # Abrimos el archivo en modo escritura
    with open(file_path, 'w') as file:
        # Iteramos sobre los inmuebles obtenidos
        for inmueble in inmuebles:
            nombre = inmueble['nombre']
            descripcion = inmueble['descripcion']
            comuna = inmueble['direccion_id__comuna_id__nombre'] #accede al nombre de la comuna.

            # Escribimos los detalles del inmueble en el archivo
            file.write(f"Comuna: {comuna}\n")
            file.write(f"    {nombre}: {descripcion}\n")
            file.write("\n") # agrega un salto de linea entre comunas para mejor legibilidad

    # Devolvemos el archivo generado
    return file_path
#desde la shell: 
#>>> from inmofacil_app.service import listar_inmuebles_por_comuna
#>>> archivo_generado = listar_inmuebles_por_comuna()
#>>> print(f"Archivo generado: {archivo_generado}") retorna archivo geneardo y el nombre del archivo ('inmuebles_por_comuna.txt')
#Archivo generado: inmuebles_por_comuna.txt

# Función para listar inmuebles por región y guardar en un archivo de texto
def listar_inmuebles_por_region():
    inmuebles = Inmueble.objects.values('nombre', 'descripcion', 'direccion_id__comuna_id__region_id__nombre') #accede al nombre de la región (direccion tiene llave foránea de comuna y comuna tiene llave foránea de region pudiendo acceder a su nombre)
    
    file_path = 'inmuebles_por_region.txt'
    
    # Abrimos el archivo en modo escritura
    with open(file_path, 'w') as file:
       
        # Iteramos sobre los inmuebles obtenidos
        for inmueble in inmuebles:
            nombre = inmueble['nombre']
            descripcion = inmueble['descripcion']
            region = inmueble['direccion_id__comuna_id__region_id__nombre']
            
            # Escribimos los detalles del inmueble en el archivo
            file.write(f"Región: {region}\n")
            file.write(f"    {nombre}: {descripcion}\n")
            file.write("\n")
            
    # Devolvemos el archivo generado
    return file_path

#desde la shell
#>>> from inmofacil_app.service import listar_inmuebles_por_region
#>>> archivo_generado = listar_inmuebles_por_region()
#>>> print(f"Archivo generado: {archivo_generado}")
#Archivo generado: inmuebles_por_region.txt