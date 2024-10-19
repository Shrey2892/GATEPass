from django.apps import AppConfig
from mongoengine import connect


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App'


    def ready(self):
        connect(
            db='User',
            host='localhost',
            port=27017,
            username='admin',
            password='Shreya123',
        )