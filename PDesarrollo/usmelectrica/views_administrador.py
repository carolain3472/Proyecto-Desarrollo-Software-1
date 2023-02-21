from django.shortcuts import render, redirect
from .models import *
from .forms import editForm
from paypal.standard.forms import PayPalPaymentsForm
import datetime


def administrador_inicio(request):
    return render(request, "social/administrador_inicio.html")

def administrador(request):
    tipo_usuario='gerente'
    usuarios = Gerente.objects.all()

    if(request.method=='POST'):
        tipo_usuario =  request.POST['tipousuario']
        if(tipo_usuario == 'gerente'):
            usuarios = Gerente.objects.all()
            id = request.POST['id']
            if id:
                usuarios = Cliente.objects.filter(pk=id)
        if(tipo_usuario == 'operador'):
            usuarios = Operador.objects.all()
            id = request.POST['id']
            if id:
                usuarios = Cliente.objects.filter(pk=id)
        if(tipo_usuario == 'cliente'):
            usuarios = Cliente.objects.all()
            id = request.POST['id']
            if id:
                usuarios = Cliente.objects.filter(pk=id)
        

    
    return render(request, "social/administrador.html", {'usuarios': usuarios, 'tipoUsuario': tipo_usuario})

def admin_crear(request):
    if request.method =='POST':
        ##crear gerentes
        if(request.POST['tipousuario']=="gerente"):
            gerente = Gerente(id_gerente= int(request.POST['id']), 
                        tipo_id_gerente= request.POST['tipoid'],  
                        celular_gerente= request.POST['celular'], 
                        nombre_gerente= request.POST['nombre'], 
                        apellidoP_Gerente= request.POST['apellidoP'],
                        apellidoM_Gerente= request.POST['apellidoM'],
                        email_gerente= request.POST['email'],
                        direccion_gerente= request.POST['direccion'],
                        contrasena_gerente= request.POST['contra'])
            gerente.save()    

        ##crear operadores
        if(request.POST['tipousuario']=="operador"):
            operador = Operador(id_operador= int(request.POST['id']), 
                        tipo_id_operador= request.POST['tipoid'],  
                        celular_operador= request.POST['celular'], 
                        nombre_operador= request.POST['nombre'], 
                        apellidoP_Operador= request.POST['apellidoP'],
                        apellidoM_Operador= request.POST['apellidoM'],
                        email_operador= request.POST['email'],
                        direccion_operador= request.POST['direccion'],
                        contrasena_operador= request.POST['contra'])
            operador.save() 
  
        ##crear clientes

        if(request.POST['tipousuario']=="cliente"):
            if (request.POST['tipoid']=="NIT"):
                persona= "Juridica"
            else:
                persona="Natural"
            cliente = Cliente(id_cliente= int(request.POST['id']), 
                        tipo_id_cliente= request.POST['tipoid'],  
                        celular_cliente= request.POST['celular'], 
                        nombre_cliente= request.POST['nombre'],
                        apellidoP_Cliente= request.POST['apellidoP'],
                        apellidoM_Cliente= request.POST['apellidoM'], 
                        email_cliente= request.POST['email'],
                        tipo_cliente= persona,
                        direccion_cliente= request.POST['direccion'],
                        contrasena_cliente= request.POST['contra'])
            cliente.save() 
            print(cliente.save())
             


        return redirect('admin')
    return render(request, "social/registro.html")

    
def admin_actualizar_gerente1(request, user_id):
    gerente= Gerente.objects.filter(id_gerente = user_id)
    
    if request.method =='POST':
        gerente.update(nombre_gerente= request.POST['nombre'])
        gerente.update(apellidoP_Gerente= request.POST['apellidoP'])
        gerente.update(apellidoM_Gerente= request.POST['apellidoM'])
        gerente.update(email_gerente= request.POST['email'])
        gerente.update(celular_gerente= request.POST['celular'])
        gerente.update(direccion_gerente= request.POST['direccion'])
        gerente.update(contrasena_gerente= request.POST['contra'])
        return redirect('admin')
    return render(request, "social/actualizar_gerente1.html", {'gerente':gerente.first()})

def admin_actualizar_cliente(request, user_id):
    
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
        return redirect('admin')
    return render(request, "social/actualizar_cliente.html", {'cliente':cliente.first()})

def admin_actualizar_operador(request, user_id):
    operador= Operador.objects.filter(id_operador = user_id)
    if request.method =='POST':
        operador.update(nombre_operador= request.POST['nombre'])
        operador.update(apellidoP_Operador= request.POST['apellidoP'])
        operador.update(apellidoM_Operador= request.POST['apellidoM'])
        operador.update(email_operador= request.POST['email'])
        operador.update(celular_operador= request.POST['celular'])
        operador.update(direccion_operador= request.POST['direccion'])
        operador.update(contrasena_operador= request.POST['contra'])
        return redirect('admin')
    return render(request, "social/actualizar_operador.html", {'operador':operador.first()})


def admin_borrar_clientes(request, user_id):
    cliente= Cliente.objects.filter(id_cliente = user_id)
    estado = cliente.first().estado_cliente
    cliente.update(estado_cliente= (not estado))
    return redirect('admin')

def admin_borrar_operadores(request, user_id):
    operador = Operador.objects.filter(id_operador = user_id)
    estado = operador.first().estado_operador
    operador.update(estado_operador= (not estado))
    return redirect('admin')

def admin_borrar_gerentes(request, user_id):
    gerente= Gerente.objects.filter(id_gerente = user_id)
    estado = gerente.first().estado_gerente
    gerente.update(estado_gerente= (not estado))
    return redirect('admin')

def admin_borrar_clientes(request, user_id):
    cliente= Cliente.objects.filter(id_cliente = user_id)
    estado = cliente.first().estado_cliente
    cliente.update(estado_cliente= (not estado))
    return redirect('admin')


def crear_servicio_admin(request, user_id):

    cliente= Cliente.objects.filter(id_cliente = user_id)
    

    if request.method=='POST':
        
        servicio = Servicio(
                        cliente_id= cliente.first(), 
                        tipo_servicios= request.POST['tiposervicio'],  
                        direccion_servicio= request.POST['direccionServicio'], 
                        fecha_creacion =  datetime.datetime.strptime(str(2022)+'/'+str(12)+'/'+str(27), '%Y/%m/%d')
                        )
        servicio.save() 
        return redirect('admin')

    return render(request, "social/crearServicio_admin.html", {'cliente':cliente.first() })


