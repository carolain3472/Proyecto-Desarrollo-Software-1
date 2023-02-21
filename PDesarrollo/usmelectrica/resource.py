
from import_export import resources 
from .models import Pago

class PagoResource(resources.ModelResource):
    class Meta:
        model=Pago