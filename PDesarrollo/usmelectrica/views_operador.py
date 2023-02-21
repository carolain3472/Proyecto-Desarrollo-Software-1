from django.shortcuts import render, redirect
from .models import *
from .forms import editForm
import datetime
from .resource import PagoResource
from tablib import Dataset
from paypal.standard.forms import PayPalPaymentsForm

import math


def operador_inicio(request, user_id):
    operadores= Operador.objects.filter(id_operador = user_id)
    return render(request, "social/operador_inicio.html", {'operadores':operadores.first()} )

def operador_registroPagos(request, user_id):
    pagos = Pago.objects.all()
    print(pagos)
    operadores= Operador.objects.filter(id_operador = user_id)

    if request.method == "POST":
        id = request.POST['id']
        if id:
            pagos = Pago.objects.filter(factura_id = id)


    return render(request, "social/operador_registroPagos.html", {'pagos':pagos, 'operadores':operadores.first()})

def importar(request, user_id):

    operadores= Operador.objects.filter(id_operador = user_id)
    #template = loader.get_template('registrarPagoBanco.html') 
    if request.method == 'POST': 
         print("Entro al Post")

         pago_resource = PagoResource() 
         dataset = Dataset()
         nuevos_pagos= request.FILES['xlsfile'] 
         imported_data = dataset.load(nuevos_pagos.read())
         print(dataset)

         result = pago_resource.import_data(dataset, dry_run=True) 
         # Test the data import  
         print(result.has_errors()) 
         print(dataset[0]) #Retorna la primer fila
         print(dataset.height)

         diccionario=[]

         for fila in range(1, dataset.height+1):
          diccionario.append(operadores.first().id_operador)
         print(diccionario)
         print(datetime.datetime.now())
         dataset.append_col(diccionario, header='operador_id')

         if not result.has_errors(): 
            for i in dataset:
                id_fact=i[3]
                factura=Factura.objects.filter(id = id_fact)
                factura.update(estado_factura=True)

            pago_resource.import_data(dataset, dry_run=False) # Actually import now

    return render(request, "social/registrarPagoBanco.html", {'operadores':operadores.first()}  ) 




def operador_registroPagos_form (request, user_id):

    operadores= Operador.objects.filter(id_operador = user_id)
    facturas = Factura.objects.all()

    if request.method =='POST':
        ##Registrar pago
        factura=Factura.objects.filter(id = request.POST['id_factura'])
        servicio= Servicio.objects.filter(id= factura.first().id_servicio_id)

        if (factura.first().estado_factura==False and (not servicio.first().mora_servicio)):
            print("No esta en mora, primer caso")
            pago = Pago( 
                            factura_id_id= request.POST['id_factura'], 
                            operador_id_id= operadores.first().id_operador,  
                            fecha_pago= datetime.datetime.now().date(), 
                            forma_pago= "Presencial", 
                            total_pago= int(request.POST['total_pago'])
                            #Poner en total_pago, el valor que hay de la factura y pensar el pago
                        )
            pago.save()
            facturaPaga= Factura.objects.filter(id = pago.factura_id_id)
            facturaPaga.update(estado_factura=True)
            print(facturaPaga)

        if (factura.first().estado_factura==False and  servicio.first().mora_servicio and (servicio.first().estado_servicio==True)):
            print(facturas.filter(id_servicio_id = servicio.first().id))
            facturasVencidas =  facturas.filter(id_servicio_id = servicio.first().id, estado_factura = False)
            total_facturas = facturasVencidas.first().total_factura + facturasVencidas.last().total_factura
            print(total_facturas)

            print("Esta en mora")
            
            pago = Pago( 
                            factura_id_id= request.POST['id_factura'], 
                            operador_id_id= operadores.first().id_operador,  
                            fecha_pago= datetime.datetime.now().date(), 
                            forma_pago= "Presencial", 
                            total_pago= int(total_facturas)
                            #Poner en total_pago, el valor que hay de la factura y pensar el pago
                        )
            pago.save()

            facturaPaga= Factura.objects.filter(id = pago.factura_id_id)
            facturaPaga.update(estado_factura=True)
            facturasVencidas.update(estado_factura=True)
            servicio.update(mora_servicio=False)
            
            print(facturaPaga)

        if (factura.first().estado_factura==False and   servicio.first().mora_servicio and (servicio.first().estado_servicio== False)):
            facturasPendientes=  facturas.filter(id_servicio_id = servicio.first().id, estado_factura = False)
            total_pagar_facturas = facturasPendientes.first().total_factura + facturasPendientes.last().total_factura
            print(total_pagar_facturas)

            print("Esta suspendido")
            
            pago = Pago( 
                            factura_id_id= request.POST['id_factura'], 
                            operador_id_id= operadores.first().id_operador,  
                            fecha_pago= datetime.datetime.now().date(), 
                            forma_pago= "Presencial", 
                            total_pago= total_pagar_facturas
                        )
            pago.save()
 

            facturasPendientes.update(estado_factura=True)
            servicio.update(estado_servicio=True)
            servicio.update(mora_servicio=False)

        return redirect('operador_registroPagos', operadores.first().id_operador)
    return render(request, "social/registrarPago.html", {'operadores':operadores.first(), 'facturas': facturas})



def operador(request, user_id):
    clientes = Cliente.objects.all()
    operadores= Operador.objects.filter(id_operador = user_id)

    if(request.method=='POST'):
        id = request.POST['id']
        if id:
            clientes = Cliente.objects.filter(pk=id)


    return render (request, "social/operador.html", {'clientes': clientes, 'operadores': operadores.first() })


def crear (request, user_id):

    if request.method =='POST':
        ##crear clientes
        
        cliente = Cliente(id_cliente= int(request.POST['id']), 
                        tipo_id_cliente= request.POST['tipoid'],  
                        celular_cliente= request.POST['celular'], 
                        nombre_cliente= request.POST['nombre'], 
                        apellidoP_Cliente= request.POST['apellidoP'],
                        apellidoM_Cliente= request.POST['apellidoM'],
                        email_cliente= request.POST['email'],
                        direccion_cliente= request.POST['direccion'],
                        contrasena_cliente= request.POST['contra'])
        cliente.save() 
        return redirect('operador', user_id)

    return render(request, "social/registro_cliente.html")



def operador_borrar_clientes(request, user_id):
    cliente= Cliente.objects.filter(id_cliente = user_id)
    estado = cliente.first().estado_cliente
    cliente.update(estado_cliente= (not estado))
    return redirect('operador')

def operador_actualizar_cliente(request, user_id):

    cliente= Cliente.objects.filter(id_cliente = user_id)

    if request.method =='POST':
        if request.POST['tipoid'] == 'C.C':
            cliente.update(apellidoP_Cliente= request.POST['apellidoP'])
            cliente.update(apellidoM_Cliente= request.POST['apellidoM'])

        
        cliente.update(nombre_cliente= request.POST['nombre'])
        cliente.update(email_cliente= request.POST['email'])
        cliente.update(celular_cliente= request.POST['celular'])
        cliente.update(direccion_cliente= request.POST['direccion'])
        cliente.update(contrasena_cliente= request.POST['contra'])
        return redirect('operador')
    return render(request, "social/actualizar_cliente.html", {'cliente':cliente.first()})

def crear_servicio(request, user_id, operador_id):
    cliente= Cliente.objects.filter(id_cliente = user_id)
    operador= Operador.objects.filter(id_operador = operador_id)

    if request.method=='POST':
        
        servicio = Servicio(
                        cliente_id= cliente.first(), 
                        tipo_servicios= request.POST['tiposervicio'],  
                        direccion_servicio= request.POST['direccionServicio'] 
                        )
        servicio.save() 
        return redirect('operador', operador_id)

    return render(request, "social/crearServicio.html", {'cliente':cliente.first(), 'operador': operador.first() })

