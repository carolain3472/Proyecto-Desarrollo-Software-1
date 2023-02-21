from django.shortcuts import render, redirect
from .models import *
from .forms import editForm
import datetime
from paypal.standard.forms import PayPalPaymentsForm

def gerente_inicio(request):
    return render(request, "social/gerente_inicio.html")

def gerente(request):
    usuarios = Administrador.objects.all()

    if(request.method=='POST'):
        if(request.POST['tipousuario'] == 'administrador'):
            usuarios = Administrador.objects.all()
            id = request.POST['id']
            if id:
                usuarios = Administrador.objects.filter(pk=id)

        if(request.POST['tipousuario'] == 'operador'):
            usuarios = Operador.objects.all()
            id = request.POST['id']
            if id:
                usuarios = Operador.objects.filter(pk=id)

        if(request.POST['tipousuario'] == 'cliente'):
            usuarios = Cliente.objects.all()
            id = request.POST['id']
            if id:
                usuarios = Cliente.objects.filter(pk=id)

    
        return render(request,"social/gerente.html", {'usuarios': usuarios, 'tipoUsuario': request.POST['tipousuario'] } )

    
    return render(request, "social/gerente.html", {'usuarios': usuarios, 'tipoUsuario': 'administrador'})

def reporte_cliente(request):
    clientes = Cliente.objects.all()
    fecha = str(datetime.datetime.now().date())
    if (request.method=='POST'):
        id = request.POST['id']
        if id:
            clientes = Cliente.objects.filter(pk=id)

    return render(request, "social/gerente_reporte_cliente.html", {'usuarios':clientes, 'fecha':fecha})

def pdf_reporte_cliente(request, user_id):
    cliente = Cliente.objects.filter(pk=user_id).first()
    desde = datetime.datetime.strptime(request.POST['inicio'], '%Y-%m').date()
    hasta = datetime.datetime.strptime(request.POST['fin'], '%Y-%m').date()

    servicios_cliente = Servicio.objects.filter(cliente_id = cliente)
    lista=[]
    for servicio in servicios_cliente:
        
        facturas = Factura.objects.filter( date_crea_factu__range=[str(desde), str(hasta)], id_servicio=servicio)
        print(facturas)
        servicio_facturas = {'servicio':servicio, 'facturas': facturas}
        lista.append(servicio_facturas)
        print(lista)

    return render(request, "social/pdf_consumo_cliente.html", {'cliente': cliente, 'facturasServicios':lista , 'desde':desde, 'hasta':hasta })
