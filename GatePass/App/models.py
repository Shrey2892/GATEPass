from mongoengine import Document, StringField, BooleanField, DateTimeField
from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# Create your models here.
class User(Document): #create a collection
    name = StringField(required=True)#field 'name'
    email = StringField(required=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    terms_accepted = BooleanField(default=False)



class Gatepass(Document):
    visitor_name = StringField(required=True)
    purpose = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)  # Automatically set current date and time

    def __str__(self):
        return f"{self.visitor_name} - {self.purpose} ({self.created_at})"    