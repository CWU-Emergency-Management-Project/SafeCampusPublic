from django.apps import AppConfig
import threading
import multiprocessing
import logging

logging.basicConfig(level=logging.DEBUG)

class WebappConfig(AppConfig):
    name = 'webapp'
    default_auto_field = 'django.db.models.BigAutoField'


    """def ready(self):
        from webapp.OccupancyEst import getEst
        t = threading.Thread(target=getEst)
        t.start()"""