from django import forms
from .models import CustomUser, DetallePedido, PedidoCliente, Producto


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class RegistroForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'rut', 'nombre_completo']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['cliente', 'despacho', 'productos', 'precio', 'cantidad','forma_pago']

class PedidoClienteForm(forms.ModelForm):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = PedidoCliente
        fields = ['cliente','direccion_entrega','fecha_pedido','forma_pago', 'productos', 'cantidad']