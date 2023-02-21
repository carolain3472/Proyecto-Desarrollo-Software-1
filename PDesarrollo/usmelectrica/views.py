from django.shortcuts import render, redirect
from .models import *
import datetime
from dateutil import relativedelta
from paypal.standard.forms import PayPalPaymentsForm
from dateutil.relativedelta import relativedelta
import random
from django.db.models import F
import requests

from django.contrib import messages

from email.message import EmailMessage
import ssl
import smtplib

# Create your views here.
#CC, Contraseña, Tipo 
def loginApp(request):
    if request.method =='POST':

        suspender_servicios()
        poner_mora()
        #generar_facturas()
        
        id = int(request.POST['user'])
        contra = request.POST['contra']

        #reCaptcha
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
            'secret': '6LefN0EkAAAAACLrZPxmqaBt-B8e6UpI1oCn5Rl-',
            'response': request.POST.get('g-recaptcha-response'),
            'remoteip': request.META.get('REMOTE_ADDR')
        })
        result = response.json()
        print("aqui ta:")
        print(result)
        if result['success']:
            ##Administrador
            if request.POST['tipousuario']=='admin':
                admin = Administrador.objects.filter(id_admin= id, contrasena_admin= contra)
                if admin.exists():
                    return redirect('admin_inicio')

            ##Gerente
            if request.POST['tipousuario']=='gerente':
                gerente = Gerente.objects.filter(id_gerente= id, contrasena_gerente= contra)
                if gerente.exists():
                    return redirect('gerente_inicio') 

            ##Operador
            if request.POST['tipousuario']=='operador':
                operador = Operador.objects.filter(id_operador= id, contrasena_operador= contra)
                if operador.exists():

                    return redirect('operador_inicio', id)        

            ##Cliente
            if request.POST['tipousuario']=='cliente':
                cliente = Cliente.objects.filter(id_cliente= id, contrasena_cliente= contra)
                if cliente.exists():
                    return redirect('cliente_inicio', id) 
        
        else:
            messages.error(request, 'Por favor, marque la casilla "No soy un robot"')
            return render(request, 'social/login.html')

    return render(request, 'social/login.html')


def suspender_servicios():
    servicios= Servicio.objects.all()
    for servicio in servicios:
        if (servicio.mora_servicio and servicio.estado_servicio):
            if (not(buscar_ultima_factura(servicio))):
                print("Dios, ayuda, plisss")
                facturas_servicio= Factura.objects.filter(id_servicio_id= servicio.id, estado_factura = False)
                facturas_servicio.update(total_factura = F('total_factura')*1.02)                
                query=Servicio.objects.filter(pk=servicio.pk)
                query.update(estado_servicio=False)
                
                


def buscar_ultima_factura(servicio):
    facturas_servicio= Factura.objects.filter(id_servicio_id= servicio.id)
    if(facturas_servicio.exists()):

        fecha_vencimiento=facturas_servicio.last().date_ven_factu
        return datetime.datetime.now().date()>fecha_vencimiento
    return True




def poner_mora():
    servicios= Servicio.objects.all()
    for servicio in servicios:
        if (not(buscar_ultima_factura(servicio))):
            print("Dios, ayuda, plisss")
            query=Servicio.objects.filter(pk=servicio.pk)
            query.update(mora_servicio=True)



def generar_facturas(): 
    servicios = Servicio.objects.all()
    for servicio in servicios: 
        dia= str(servicio.fecha_creacion.day)
        mes= str(datetime.datetime.now().month)
        ano= str(datetime.datetime.now().year)
        fecha_generar = datetime.datetime.strptime(ano+'/'+mes+'/'+dia, '%Y/%m/%d')
        #true si hay facturas, false si no hay
        factura = bool(Factura.objects.filter(id_servicio = servicio.pk, date_crea_factu = fecha_generar).first())
        
        if fecha_generar.date() == datetime.datetime.now().date() and not factura and not servicio.mora_servicio:
            ##crea una nueva factura 
            consumoAleatorio = random.randint(10,700)
            factura = Factura(
                id_servicio = Servicio.objects.filter(pk=servicio.pk).first(),
                consumo_factura = consumoAleatorio,
                lectura_factura = 30,
                total_factura = 778*consumoAleatorio,
                date_crea_factu = datetime.datetime.now().date(),
                date_ven_factu = datetime.datetime.now() + relativedelta(days =+ 10), 
                periodo_factu = datetime.datetime.now() - relativedelta(month = 1),
            )
            
            factura.save()


def enviarCorreo():
    email_sender= 'carolain.jimenez@correounivalle.edu.co'
    email_password= 'amzcqwgkqhdijrvh'
    email_receiver= 'carolain403@gmail.com'
    subject= 'REVISA TU FACTURA'
    body = """Buenas tarde señor@, nos comunicamos desde la compañia usm electrica para notificar el envio de su factura, por favor, ingrese a la página y descargue su factura."""
    em = EmailMessage()
    em['From']= email_sender
    em['To']= email_receiver
    em['Subject']= subject
    em.set_content(body)
    
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender,email_receiver, em.as_string())
