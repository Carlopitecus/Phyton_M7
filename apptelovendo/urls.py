from django.urls import path
from . import views 


urlpatterns = [
    path('', views.index, name='index'),
    path('registro/',views.registro_usuario, name= 'registro'),
    path('bienvenida/', views.bienvenida, name= 'bienvenida'),
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('sesion_iniciada/', views.sesion_iniciada, name='sesion_iniciada'),
    path('exit/', views.exit, name = 'exit'),
    path('verPedidos/', views.verPedidos, name = 'verPedidos'),
    path('detalle_pedido/<int:pedido_id>/', views.detalle_pedido, name= 'detalle_pedido'),
    path('tomar_pedido', views.tomar_pedido, name='tomar_pedido'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('categorias/',views.categorias, name='categorias'),
    path('realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('mis_pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('cancelar_pedido/<int:pedido_id>/', views.cancelar_pedido, name='cancelar_pedido')    
]