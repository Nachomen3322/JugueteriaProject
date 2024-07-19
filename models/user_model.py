from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# usando herencia
class User(UserMixin, db.Model):
    __tablename__ = "users"
    #nombre apellido email,username, celular, direccion, ciudad, pais

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(59), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    celular = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    ciudad = db.Column(db.String(50), nullable=False)
    pais = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")

    def __init__(self, nombre, apellido, username, celular, direccion, ciudad, pais, password, role="user"):
        self.nombre = nombre
        self.apellido = apellido
        self.username = username
        self.celular = celular
        self.direccion = direccion
        self.ciudad = ciudad
        self.pais = pais    
        self.set_password(password)
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def has_role(self, role):
        return self.role == role
