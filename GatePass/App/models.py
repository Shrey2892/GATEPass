from mongoengine import Document, StringField, BooleanField
# from werkzeug.security import generate_password_hash, check_password_hash
# Create your models here.
class User(Document): #create a collection
    name = StringField(required=True)#field 'name'
    email = StringField(required=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    terms_accepted = BooleanField(default=False)

     