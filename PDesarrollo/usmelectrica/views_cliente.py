
import unicodedata
from django.shortcuts import render, redirect
from .models import *
from .forms import editForm
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponse, JsonResponse
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest, OrdersCaptureRequest
import sys, json



def clientes(request, user_id):
    usuario = Cliente.objects.filter(pk=user_id)
    return render(request, "social/cliente_inicio.html", {'usuario':usuario.first()})

def pagoCliente(request, servicio_id):
    servicio= Servicio.objects.filter(pk= servicio_id).first()
    factura = Factura.objects.filter(id_servicio=servicio_id)
    return render(request, "social/pagoCliente.html", {'servicio':servicio, 'factura':factura.last()})

def verFactura(request, user_id):
    usuario = Cliente.objects.filter(pk=user_id)
    servicios = Servicio.objects.filter(cliente_id=usuario.first().id_cliente)
    return render(request, "social/verFactura_Servicios.html", {'usuario':usuario.first(), 'servicios': servicios })

def verPDFFactura(request, servicio_id):
    servicio= Servicio.objects.filter(pk= servicio_id).first()
    cliente = Cliente.objects.filter(pk= servicio.cliente_id_id ).first()
    facturas = Factura.objects.all()
    facturasPendientes=  facturas.filter(id_servicio_id = servicio.id, estado_factura = False)   
    total = 0
    for factura in facturasPendientes: 
        total += factura.total_factura

    return render(request, "social/facturaCliente.html", {'factura': facturasPendientes.last(), 'cliente':cliente, 'servicio':servicio, 'facturas':facturasPendientes, 'total':total})

def pago(request, servicio_id):
    #factura, de donde se sacara el precio
    factura = Factura.objects.filter(pk=servicio_id)
    print(factura)
    total_pagar_facturas = factura.first().total_factura

    servicio= Servicio.objects.filter(pk= servicio_id).first()

    curso=Producto.objects.get(pk=1) #Pasar la llave de la factura a pagar

    data= json.loads(request.body)
    order_id= data['orderID']

    detalle= GetOrder().get_order(order_id)
    detalle_precio= float(detalle.result.purchase_units[0].amount.value)
    print(detalle_precio)
    print("Holaaa")

    if detalle_precio== total_pagar_facturas:
        print("Diosito ayudaaaa ota vez")
        trx= CaptureOrder().capture_order(order_id, debug=True)

        #Se añade a pago
        pago= Pago(
                            factura_id_id= factura.last().id,  
                            fecha_pago= datetime.datetime.now().date(), 
                            forma_pago= "Virtual", 
                            total_pago= total_pagar_facturas
        )
        pago.save()

        

        data= {
            "id": f"{trx.result.id}",
            "nombre_cliente": f"{trx.result.payer.name.given_name}",
            "mensaje": "Se ha realizado con exito la transacción"
        }

        return JsonResponse(data)
    else:
        data= {
            
            "mensaje": "ERROR"
        }

        return JsonResponse(data)
        

class payPalClient:
    def __init__(self):
        self.client_id= "AR1ReLSU1hsMq2qaWDgE81XOl0Czj3wS_5Vpbevl-lQK8N4EAm4rd1Phm2qoFMjQJWXN3KxRXpWhpj1S"
        self.client_secret= "EDSszL9P2pRhcSOAthUwyVGkJpbXRlamQEIwlc4IG3cKUMIr3r0aUzQeEKCRVsX8TxPHIriOoKBmYLDg"
        self.environment=SandboxEnvironment(client_id=self.client_id,client_secret=self.client_secret)
        self.client=PayPalHttpClient(self.environment)

    def object_to_json(self,json_data):
        result={}
        if sys.version_info[0]<3:
            itr= json_data.__dict__.iteritems()
        else:
            itr= json_data.__dict__.items()
        for key,value in itr:
            if key.startswith("__"):
                continue
            result[key]= self.array_to_json_array(value) if isinstance(value, list) else\
                self.object_to_json(value) if not self.is_primittive(value) else\
                    value
        return result

    def array_to_json_array(self, json_array):
        result=[]
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if not 
                self.is_primittive(item)\
                    else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, unicodedata) or isinstance(data, int)


class  GetOrder(payPalClient):
    def get_order(self, order_id):
        request= OrdersGetRequest(order_id)
        response= self.client.execute(request)
        return response

    #    print ('Status Code: ', response.status_code)
     #   print ('Status: ', response.result.status)
      #  print ('Order ID: ', response.result.id)
       # print ('Intent: ', response.result.intent)
        #print ('Links: ')
        #for link in response.result.links:
         #   print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
          #  print('Gross Amount: {} {}'.format(response.result.purchase_units[0].amount.currency_code, response.result.purchase_units[0].amount.value))

#if __name__=='__main__':
 #   GetOrder().get_order('REPLACE-WITH-VALID-ORDER-ID')

class CaptureOrder(payPalClient):

    def capture_order(self, order_id, debug=False):
        request= OrdersCaptureRequest(order_id)
        response= self.client.execute(request)

        if debug:
            print ('Status Code: ', response.status_code)
            print ('Status: ', response.result.status)
            print ('Order ID: ', response.result.id)
            print ('Links: ')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            print('Capture Ids: ')
            for purchase_unit in response.result.purchase_units:
                for capture in purchase_unit.payments.captures:
                    print ('\t', capture.id)
            print("Buyer:")

        return response 

#if __name__=='__main__':
 #   order_id= 'REPLACE-WITH-APPORVED-ORDER-ID'
  #  CaptureOrder().capture_order(order_id, debug=True)








        

    
