from django.db import models
from mongoengine import Document, StringField, IntField
# Create your models here.
class User(Document):
    name = StringField(required=True, default="")
    email = StringField(default="")
    username = StringField(required=True,default="")
    pwd = StringField(required=True)
    

     