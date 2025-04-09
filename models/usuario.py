from mongoengine import Document, StringField

class Usuario(Document):
    usuario = StringField(max_length=50, unique=True, required=True)
    password = StringField(max_length=255, required=True)
    nombre = StringField(max_length=100, required=True)
    correo = StringField(max_length=100, required=True, unique=True)

    def __repr__(self):
        return self.usuario
