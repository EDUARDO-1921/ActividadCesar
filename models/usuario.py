from mongoengine import *

class Usuario(Document):
    usuario = StringField(max_length=50, unique=True, required=True)
    password = StringField(required=True)
    nombre_completo = StringField(max_length=100, required=True)
    correo_electronico = EmailField(required=True)
    
    def __repr__(self):
        return self.usuario