from mongoengine import *
from models.genero import Genero

class Pelicula(Document):
    titulo = StringField(required=True, max_length=50)
    codigo = IntField(required=True, unique=True)
    descripcion = StringField(max_length=200)
    genero = ReferenceField(Genero, reverse_delete_rule=DENY, required=True)
    duracion = IntField(required=True, min_value=30, max_value=300)
    foto = StringField()
    resumen = StringField(required=True)
    protagonistas = ListField(StringField(max_length=50), required=True)
    
    def __str__(self):
        return self.titulo