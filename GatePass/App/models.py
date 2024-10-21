from mongoengine import Document, StringField, BooleanField, DateTimeField,IntField
from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# Create your models here.
class User(Document): #create a collection
    name = StringField(required=True)#field 'name'
    email = StringField(required=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    terms_accepted = BooleanField(default=False)

    meta = {'collection': 'user'}



class Gatepass(Document):
    gatepassno =IntField(required=True)
    driver_name = StringField(required=True)
    purpose = StringField(required=True)
    vehicle_number=StringField(required=True)
    owner_contact_no=IntField(required=True)
    Access_Area=StringField()

    created_at = DateTimeField(default=datetime.now) #DateTimeField(default=datetime.now)  # Automatically set current date and time
    
    def __str__(self):
        return self.gatepassno
    meta = {'collection': 'gatepass'}
    # def __str__(self):
    #     return f"{self.visitor_name} - {self.purpose} ({self.created_at})"    

    