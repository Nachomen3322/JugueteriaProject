from flask import Blueprint, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.jueguete_model import Juguete
from views import juguete_view
from utils.decorators import role_required

# Crear un blueprint para el controlador de juguetes
juguete_bp = Blueprint("juguete", __name__)

#nombre, tipo, cantidad, precio

@juguete_bp.route("/juguetes")
@login_required
def list_juguetes():
    juguetes = Juguete.get_all()
    return juguete_view.list_juguetes(juguetes)


@juguete_bp.route("/juguetes/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create_juguete():
    if request.method == "POST":
        if current_user.has_role("admin"):
            nombre = request.form["nombre"]
            tipo = request.form["tipo"]
            cantidad = request.form["cantidad"]
            precio = request.form["precio"]
            juguete=Juguete(nombre=nombre, tipo=tipo, cantidad=cantidad, precio=precio)
            juguete.save()
            flash("Juguete creado exitosamente", "success")
            return redirect(url_for("juguete.list_juguetes"))
        else:
            return jsonify({"message": "Unauthorized"}), 403
    return juguete_view.create_juguete()


@juguete_bp.route("/juguetes/<int:id>/update", methods=["GET", "POST"])
@login_required
@role_required("admin")
def update_juguete(id):
    juguete = Juguete.get_by_id(id)
    if not juguete:
        return "Juguete no encontrado", 404
    if request.method == "POST":
        if current_user.has_role("admin"):
            nombre = request.form["nombre"]
            tipo = request.form["tipo"]
            cantidad = int(request.form["cantidad"])
            precio = float(request.form["precio"])
            juguete.update(nombre=nombre, tipo=tipo, cantidad=cantidad, precio=precio)
            flash("Juguete actualizado exitosamente", "succsess")
            return redirect(url_for("juguete.list_juguetes"))
        else:
            return jsonify({"message": "Unauthorized"}), 403
    return juguete_view.update_juguete(juguete)


# Ruta para eliminar un juguete existente
@juguete_bp.route("/juguetes/<int:id>/delete")
@login_required
@role_required("admin")
def delete_juguete(id):
    juguete = Juguete.get_by_id(id)
    if not juguete:
        return "Juguete no encontrado", 404
    juguete.delete()
    return redirect(url_for("juguete.list_juguetes"))
