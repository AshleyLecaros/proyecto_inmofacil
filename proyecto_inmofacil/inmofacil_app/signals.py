from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

@receiver(post_save, sender=User)
def asignar_roles_a_usuario(sender, instance, created, **kwargs):
    """
    Función para asignar roles automáticamente a un usuario nuevo.
    Se ejecuta cada vez que se guarda un usuario.
    """
    if created:
        if instance.tipo_usuario == 'arrendador':
            arrendador_group, created = Group.objects.get_or_create(name='Arrendador')
            instance.groups.add(arrendador_group)
        elif instance.tipo_usuario == 'arrendatario':
            arrendatario_group, created = Group.objects.get_or_create(name='Arrendatario')
            instance.groups.add(arrendatario_group)