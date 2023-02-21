# Proyecto-Desarrollo

//crear carpeta en el escritorio “ProyectoDesarrollo” 

python3 -m venv desarrolloenv 

source desarrolloenv/scripts/activate

pip install django 

django-admin startproject PDesarrollo

cd PDesarrollo

python manage.py startapp usmelectrica

# Se deben descargar estas librerias:

pip install psycopg2

pip install django-import-export

pip install django-paypal

pip install tablib

pip install django-relativedelta

pip install python-dateutil

pip install paypal-checkout-serversdk
