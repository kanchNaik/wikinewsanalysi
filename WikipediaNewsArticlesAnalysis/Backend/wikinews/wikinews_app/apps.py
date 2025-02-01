from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command
import threading
#from .taskdefine import task1, task2

class WikinewsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wikinews_app'

    #def ready(self):
        #t1 = threading.Thread(target=task1, daemon=True)
        #t2 = threading.Thread(target=task2, daemon=True)

        #t1.start()
        #t2.start()
        

        