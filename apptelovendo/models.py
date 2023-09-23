from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

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



class DetallePedido(models.Model):
    #pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    #producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.IntegerField(blank=True, null=True)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    forma_pago = models.CharField(max_length=50, blank=True, null=True)
    despacho = models.CharField(max_length=250, blank=True, null=True)
    productos = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        datos = "Producto: " + self.producto.nombre
        return datos
    
class NumeroPedidoUtilizado(models.Model):
    numero_pedido = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.numero_pedido
    
class Pedido(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('preparacion', 'En preparacion'),
        ('despacho', 'En despacho'),
        ('entregado','Entregado'),
        ('cancelado', 'Cancelado')
    )


    producto = models.ManyToManyField(Producto)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name='pedidos', blank=True, null=True)
    asignado_a = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='pedidos_asinados')
    despacho = models.CharField(max_length=250, blank=True, null=True)
    forma_pago = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.estado
    
class PedidoCliente(models.Model):
    cliente = models.CharField(max_length=100, blank=True, null=True)
    direccion_entrega = models.CharField(max_length=250)
    fecha_pedido = models.DateField()
    forma_pago = models.CharField(max_length=100)
    numero_pedido = models.CharField(max_length=10, unique=True, editable=False)
    cantidad = models.PositiveIntegerField(default=1)
    productos = models.ManyToManyField(Producto)
    estado = models.ForeignKey(Pedido,blank=True, null=True,  on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.estado:
            self.estado = Pedido.objects.get(estado='pendiente')
        super(PedidoCliente, self).save(*args, **kwargs)

    def generar_numero_pedido(self):
        ultimo_pedido = NumeroPedidoUtilizado.objects.order_by('-id').first()
        if ultimo_pedido:
            ultimo_numero = int(ultimo_pedido.numero_pedido.split('-')[1])
            nuevo_numero = str(ultimo_numero + 1).zfill(3)
        else:
            nuevo_numero = "001"
        self.numero_pedido = f"PED-{nuevo_numero}"

    def __str__(self):
        return str(self.numero_pedido)
    
@receiver(pre_save, sender=PedidoCliente)
def actualizar_numero_pedido(sender, instance, **kwargs):
    if not instance.numero_pedido:
        instance.generar_numero_pedido()
        numero_pedido_utilizado =NumeroPedidoUtilizado(numero_pedido=instance.numero_pedido)
        numero_pedido_utilizado.save()

class HistorialPedido(models.Model):
    pedido = models.ForeignKey(PedidoCliente, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20)
    estado_actual = models.CharField(max_length=20, blank=True, null=True)
    
    

