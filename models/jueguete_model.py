from database import db


class Juguete(db.Model):
    __tablename__ = "Juguetes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def __init__(self, nombre, tipo, cantidad, precio):
        self.nombre = nombre
        self.tipo = tipo
        self.cantidad = cantidad
        self.precio = precio

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Juguete.query.all()

    @staticmethod
    def get_by_id(id):
        return Juguete.query.get(id)

    def update(self, nombre=None, tipo=None, cantidad=None, precio=None):
        if nombre is not None:
            self.nombre = nombre
        if tipo is not None:
            self.tipo = tipo
        if cantidad is not None:
            self.cantidad = cantidad
        if precio is not None:
            self.precio = precio
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
