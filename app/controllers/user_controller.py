from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from utils.decorators import role_required
from views import user_view
from models.user_model import User
from database import db

user_bp = Blueprint("user", __name__)


@user_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("user.profile", id=current_user.id))
    return redirect(url_for("user.login"))


@user_bp.route("/users")
@login_required
def list_users():
    users = User.get_all()
    return user_view.usuarios(users)


    

@user_bp.route("/users/create", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        username = request.form["username"]
        celular = request.form["celular"]
        direccion = request.form["direccion"]
        ciudad = request.form["ciudad"]
        pais = request.form["pais"]
        password = request.form["password"]
        role = request.form["role"]
        
        
        
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El nombre de usuario ya está en uso", "error")
            return redirect(url_for("user.create_user"))
        user = User(nombre, apellido, username, celular, direccion, ciudad, pais, password, role)
        user.set_password(password)
        user.save()
        flash("Usuario registrado exitosamente", "success")
        return redirect(url_for("user.list_users"))
    return user_view.registro()

@user_bp.route("/users/<int:id>/update", methods=["GET", "POST"])  # Asegúrate de tener esta ruta definida correctamente
@login_required
@role_required("admin")
def update_user(id):
    user = User.get_by_id(id)  # Asegúrate de que este método exista y funcione correctamente en tu modelo User
    if not user:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("user.list_users")), 404

    if request.method == "POST":
        user.nombre = request.form["nombre"]
        user.apellido = request.form["apellido"]
        user.username = request.form["username"]
        user.celular = request.form["celular"]
        user.direccion = request.form["direccion"]
        user.ciudad = request.form["ciudad"]
        user.pais = request.form["pais"]
        user.role = request.form["role"]
        user.role = password = request.form["password"]
        
        db.session.commit()  # Esto guarda los cambios en la base de datos
        flash("Usuario actualizado exitosamente", "success")
        return redirect(url_for("user.list_users"))

    return user_view.actualizar(user)



@user_bp.route("/users/<int:id>/delete")
@login_required
@role_required("admin")
def delete_user(id):
    user = User.get_by_id(id)
    if not user:
        return "Usuario no encontrado", 404
    user.delete()
    return redirect(url_for("user.list_users"))


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.get_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Inicio de sesión exitoso", "success")
            if user.has_role("admin"):
                return redirect(url_for("user.list_users"))
            else:
                return redirect(url_for("user.profile", id=user.id))
        else:
            flash("Nombre de usuario o contraseña incorrectos", "error")
    return user_view.login()


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("user.login"))


@user_bp.route("/profile/<int:id>")
@login_required
def profile(id):
    user = User.get_by_id(id)
    return user_view.perfil(user)
