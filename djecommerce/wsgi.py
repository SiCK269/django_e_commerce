import os
from whitenoise import WhiteNoise


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djecommerce.settings')

application = WhiteNoise(get_wsgi_application())
application.add_files("C:/Users/aliha/Desktop/Projects/django_e_commerce/static_in_env/")
