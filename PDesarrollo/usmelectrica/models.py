from django.db import models
import datetime



id_type = (('C.C', 'C.C'),('C.E', 'C.E'),('NIT', 'NIT'),('Pasaporte', 'Pasaporte'))
type_cliente = (('Natural', 'Natural'),('Juridica', 'Juridica'))
payment_type = (('Presencial', 'Presencial'), ('Banco', 'Banco'), ('Virtual', 'Virtual'))
zone_type = (('Residencial', 'Residencial'), ('Comercial', 'Comercial'), ('Industrial', 'Industrial'))

# Create your models here.

class Administrador(models.Model):
    id_admin = models.IntegerField(primary_key= True)
    tipo_id_admin = models.CharField(max_length = 12, choices = id_type, default='C.C')
    celular_admin = models.CharField(max_length= 16, null=True)
    nombre_admin = models.CharField(max_length = 64, null=True)
    apellidoP_admin = models.CharField(max_length = 64, null=True)
    apellidoM_admin = models.CharField(max_length = 64, null=True)
    email_admin = models.CharField(max_length = 64, null=True)
    direccion_admin = models.CharField(max_length = 64, null=True)
    contrasena_admin = models.CharField(max_length = 80, null=True)

class Operador(models.Model):
    id_operador = models.IntegerField(primary_key= True)
    tipo_id_operador = models.CharField(max_length = 12, choices = id_type, default='C.C')
    celular_operador = models.CharField(max_length= 16, null=True)
    nombre_operador = models.CharField(max_length = 64, null=True)
    apellidoP_Operador = models.CharField(max_length = 64, null=True)
    apellidoM_Operador = models.CharField(max_length = 64, null=True)
    email_operador = models.CharField(max_length = 64, null=True)
    direccion_operador = models.CharField(max_length = 64, null=True)
    contrasena_operador = models.CharField(max_length = 80, null=True)
    estado_operador = models.BooleanField(default=True)

class Gerente(models.Model):
    id_gerente = models.IntegerField(primary_key= True)
    tipo_id_gerente = models.CharField(max_length = 12, choices = id_type, default='C.C')
    celular_gerente= models.CharField(max_length= 16, null=True)
    nombre_gerente = models.CharField(max_length = 64, null=True)
    apellidoP_Gerente = models.CharField(max_length = 64, null=True)
    apellidoM_Gerente = models.CharField(max_length = 64, null=True)
    email_gerente = models.CharField(max_length = 64, null=True)
    direccion_gerente = models.CharField(max_length = 64, null=True)
    contrasena_gerente = models.CharField(max_length = 80, null=True)
    estado_gerente = models.BooleanField(default=True)


class Cliente(models.Model):
    id_cliente = models.IntegerField(primary_key= True)
    tipo_id_cliente = models.CharField(max_length = 12, choices = id_type, default='C.C')
    celular_cliente = models.CharField(max_length= 16, null=True)
    nombre_cliente = models.CharField(max_length = 64, null=True)
    apellidoP_Cliente = models.CharField(max_length = 64, null=True)
    apellidoM_Cliente = models.CharField(max_length = 64, null=True)
    email_cliente = models.CharField(max_length = 64, null=True)
    direccion_cliente = models.CharField(max_length = 64, null=True)
    contrasena_cliente = models.CharField(max_length = 80, null=True)
    estado_cliente = models.BooleanField(default=True)
    tipo_cliente = models.CharField(max_length = 12, choices = type_cliente, default='Natural')
 
class Servicio(models.Model):
    cliente_id = models.ForeignKey(Cliente, null = False, blank = False, on_delete = models.CASCADE)
    tipo_servicios = models.CharField(max_length = 12, choices = zone_type, default='Residencial')
    estado_servicio = models.BooleanField(default = True)
    mora_servicio = models.BooleanField(default = False)
    direccion_servicio= models.CharField(max_length = 64, null=True)
    fecha_creacion= models.DateField(null=False, default= '2022/12/22')


class Factura(models.Model):
    id_servicio = models.ForeignKey(Servicio, null = False, blank = False, on_delete = models.CASCADE)
    consumo_factura = models.IntegerField(null = False) #Podemos poner un consumo por defecto despues de realizar backend
    lectura_factura = models.IntegerField(null = False)
    total_factura = models.IntegerField(null = False)
    date_crea_factu = models.DateField(null = False)
    date_ven_factu = models.DateField(null = False)
    periodo_factu = models.DateField(null = False)
    estado_factura = models.BooleanField(default = False)

    


class Pago(models.Model):
    #fecha_pago = models.DateField(null = False)
    #fecha_pago= models.DateTimeField(null=True, blank=True)
    forma_pago = models.CharField(null = True, blank=True,max_length = 12, choices = payment_type, default = 'Presencial')
    total_pago = models.IntegerField(null = True, blank=True, default=0)
    factura_id =  models.ForeignKey(Factura, null = True, blank = True,  on_delete = models.CASCADE)
    operador_id = models.ForeignKey(Operador, null = True, blank=True, on_delete = models.CASCADE)
    #Hay un problema con la fecha, al hacerlo con excel, excel saca fecha y hora, por lo cual, no deja con solo fecha.
    fecha_pago = models.DateField( null = True, blank=True, default= datetime.datetime.now().date())
    #fecha_pago = models.DateField(null = True, blank=True, default='2022-12-01')
   # factura_id = models.ForeignKey(Factura, null = True, blank = True, default=1, on_ delete = models.CASCADE)
   # operador_id = models.ForeignKey(Operador, null = True, blank=True, on_delete = models.CASCADE)
   
#No es importante
class Pagoejemplo(models.Model):
    forma_pagar = models.CharField(max_length = 12)
    cedula = models.IntegerField(null = True, blank=True, default=0)
    #total_pago = models.DecimalField(max_digits=5, decimal_places=1)
    total_pago = models.CharField(max_length = 12)
    operador= models.IntegerField(null = True, blank=True, default=0)


#Pendientes:

#No puede volver a pagar dos veces la misma factura, en online
    #Si el estado de la factura es pagado (True), no puede dejar generar la transaccion (pago, online views pago), lo mismo presencial


#Si no paga en un mes y realiza un pago del otro mes, debe cargarse el valor de las dos 
    #Verificar si la factura anterior esta paga, si no está paga(False), el valor de la trasacción debe ser el de las dos facturas y al realizarse la transacció,
    #poner las dos facturas como pagas

#Quitar la mora cuando ya pague

#Para reactivar serivicio poner 2%
    #Verificar si el servicio está suspendido, si está suspendido, y se realizará  un pago, el valor debe ser las 2 facturas acumuladas
    #+ 2% de ese valor, se verifica la transacción, se pone pago(true) las dos facturas y servicio estado True


#Generar facturas automaticamente 


class Producto(models.Model):
    producto = models.CharField(max_length=100, null=False)
    precio= models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.producto



class Compra(models.Model):
    id = models.CharField(primary_key= True, max_length=100)
    estado = models.CharField(max_length = 100)
    codigo_estado = models.CharField(max_length= 100)
    producto = models.ForeignKey(to=Producto, on_delete=models.SET_NULL, null=True)
    total_de_la_compra = models.DecimalField(max_digits= 5, decimal_places=2)
    nombre_cliente = models.CharField(max_length = 64)
    apellido_cliente= models.CharField(max_length=100)
    correo_cliente = models.EmailField(max_length = 100)
    direccion_cliente = models.CharField(max_length = 64)

    def __str__(self):
        return self.nombre_cliente
