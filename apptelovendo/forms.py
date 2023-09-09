from django import forms
from .models import CustomUser, DetallePedido, Pedido

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