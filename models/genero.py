from mongoengine import *

class Genero(Document):
    nombre=StringField(max_length=50,unique=True,required=True)

    def _repr__(self):
        return self.nombre