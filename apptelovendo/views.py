from django.shortcuts import render, redirect
from .forms import RegistroForm
import random
import string
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Pedido, DetallePedido, CustomUser
from django.contrib.auth import get_user_model

#pagina de inicio
def index(request):
    return render (request, 'apptelovendo/index.html')

def exit(request):
    logout(request)
    return redirect('index')
#Formulario de registro
def registro_usuario(request):
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = generate_random_password()
            user.set_password(password)
            user.save()

            send_registration_email(user.email, password)

            return redirect('bienvenida')
    else:
        form = RegistroForm()
    return render(request, 'apptelovendo/registro.html', {'form': form})

#gnerar contraseña aleatoria
def generate_random_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(6))
    return password

#Envio de contraseña la cual se recibe por consola 
def send_registration_email(email, password):
    subject = 'Bienvenido a Te lo vendo'
    message = f'Tu contraseña para ingresar a tus pedidos es: {password}'
    from_email = 'noreply@teloVendo.com' 
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
    
#bienvenida al usuario registrado 
def bienvenida(request):
    return render(request, 'apptelovendo/bienvenida.html')

#Inicio de sesion
def iniciar_sesion(request):
    if request.method == 'POST':
        # Obtener los datos del formulario de inicio de sesión
        email= request.POST.get('username')
        password = request.POST.get('password')

        # Autenticar al usuario
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # El inicio de sesión es exitoso, redirigir a la vista sesion_iniciada
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect ('verPedidos')
            else:
                return redirect('sesion_iniciada')
        else:
            messages.error(request, 'Tu correo o contraseñas no son correctos. Por favor intenta nuevamente.')
    return render(request, 'apptelovendo/login.html')

def sesion_iniciada(request):
    return render(request, 'apptelovendo/sesion_iniciada.html')

def verPedidos(request):
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        nuevo_estado = request.POST.get('nuevo_estado')

        pedido = Pedido.objects.get(id=pedido_id)
        pedido.estado = nuevo_estado
        pedido.save()

        if pedido and pedido.usuario:
            send_notification_email(pedido, nuevo_estado)
        
    pedidos = Pedido.objects.all().order_by('id')
    return render(request, 'apptelovendo/verPedidos.html', {'pedidos':pedidos})

#Envio de actualizacion de pedidos
def send_notification_email(pedido, nuevo_estado):
    subject = 'Actualzacion del estado de su pedido'
    message = f'El estado de tu pedido numero {pedido.id} ha sido actualizado a {pedido.estado}'
    from_email = 'noreply@teloVendo.com'
    recipient_list = [pedido.usuario.email]

    send_mail(subject, message, from_email, recipient_list)

def detalle_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    detalles = pedido.detallepedido_set.all()
    return render(request, 'apptelovendo/detalle_pedido.html', {'pedido': pedido, 'detalles': detalles })  

def tomar_pedido(request):
    CustomUser = get_user_model()
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        usuario = CustomUser.objects.get(id=usuario_id)

        pedido = Pedido.objects.filter(asignado_a=None, estado='pendiente').first()
        if pedido:
            pedido.asignado_a = usuario
            pedido.save()
        
        return redirect('verPedidos')
    

    usuarios = CustomUser.objects.all()
    usuarios_con_pedidos_pendientes = CustomUser.objects.filter(pedidos__estado='pendiente').distinct()

    return render(request, 'apptelovendo/tomar_pedido.html',{'usuarios':usuarios, 'usuarios_con_pedidos_pendientes': usuarios_con_pedidos_pendientes})

