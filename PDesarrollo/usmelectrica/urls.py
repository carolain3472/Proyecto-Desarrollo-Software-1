from django.urls import path 
from . import views
from . import views_administrador, views_gerente, views_operador, views_cliente

urlpatterns= [
    path('', views.loginApp, name='login'),

    ##url administrador
    path('administrador/gestion/', views_administrador.administrador, name='admin'),
    path('administrador/', views_administrador.administrador_inicio, name='admin_inicio'),
    path('administrador/borrar_operador/<int:user_id>/', views_administrador.admin_borrar_operadores, name='admin_borrar_operadores'),
    path('administrador/borrar_gerente/<int:user_id>/', views_administrador.admin_borrar_gerentes, name='admin_borrar_gerentes'),
    path('administrador/borrar_cliente/<int:user_id>/', views_administrador.admin_borrar_clientes, name='admin_borrar_clientes'),
    path('administrador/crear/', views_administrador.admin_crear, name='admin_crear'),
    path('administrador/actualizar_gerente/<int:user_id>/', views_administrador.admin_actualizar_gerente1, name='admin_actualizar_gerente1'),
    path('administrador/actualizar_cliente/<int:user_id>/', views_administrador.admin_actualizar_cliente, name='admin_actualizar_cliente'),
    path('administrador/actualizar_operador/<int:user_id>/', views_administrador.admin_actualizar_operador, name='admin_actualizar_operador'),
    path('administrador/crearServicio/<int:user_id>/', views_administrador.crear_servicio_admin, name='crear_servicio_admin'),
   

    ##url gerente
    path('gerente/gestion/', views_gerente.gerente, name='gerente'),
    path('gerente/', views_gerente.gerente_inicio, name='gerente_inicio'),
    path('gerente/reporteCliente/', views_gerente.reporte_cliente, name='reporte_cliente'),
    path('gerente/reporteCliente/consumo/<int:user_id>/', views_gerente.pdf_reporte_cliente, name='pdf_consumo'),
    



    ##url operadores
    path('operador/<int:user_id>/', views_operador.operador_inicio, name='operador_inicio'),
    path('operador/gestion/<int:user_id>/', views_operador.operador, name='operador'),
    path('operador/borrar_cliente/<int:user_id>/', views_operador.operador_borrar_clientes, name='operador_borrar_clientes'),
    path('operador/crear/<int:user_id>/', views_operador.crear, name='operador_crear'),
    path('operador/actualizar_cliente/<int:user_id>/', views_operador.operador_actualizar_cliente, name='operador_actualizar_cliente'),
    path('operador/registroPagos/<int:user_id>/', views_operador.operador_registroPagos, name='operador_registroPagos'),
    path('operador/registroPagos_form/<int:user_id>/', views_operador.operador_registroPagos_form, name='operador_registroPagos_form'),
    path('operador/registroPagoBanco/<int:user_id>/', views_operador.importar, name='importar'),
    path('operador/crearServicio/<int:user_id>/<int:operador_id>/', views_operador.crear_servicio, name='crear_servicio'),

    ##url clientes
    path('cliente/<int:user_id>/', views_cliente.clientes, name='cliente_inicio'),
    path('pagocliente/<int:servicio_id>/', views_cliente.pagoCliente, name='pagoCliente'),
    path('pago/<int:servicio_id>/', views_cliente.pago, name='pago'),
    path('cliente/consultarFactura/<int:user_id>/', views_cliente.verFactura, name='facturacliente'),
    path('cliente/consultarFactura/Factura/<int:servicio_id>/', views_cliente.verPDFFactura, name='pdf_factura'),


    
]