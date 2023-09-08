from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    rut = models.CharField(max_length=20, unique=True)
    nombre_completo= models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.AutoField
    
    #campos para manejo de grupos y roles
    ROLES = (
        ('cliente', 'Cliente'),
        ('administrador', 'Administrador')
    )

    role = models.CharField(max_length=15, choices=ROLES, default='cliente')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['rut']

    def __str__(self):
        return self.email
    

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    descripcion = models.TextField()

class Pedido(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('preparacion', 'En preparacion'),
        ('despacho', 'En despacho'),
        ('entregado','Entregado')
    )


    producto = models.ManyToManyField(Producto)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name='pedidos')
    asignado_a = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='pedidos_asinados')

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
