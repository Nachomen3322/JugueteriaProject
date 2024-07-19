from flask import render_template
from flask_login import current_user


# La función `list_libros` recibe una lista de
# libroes y renderiza el template `libroes.html`
def list_juguetes(juguetes):
    return render_template(
        "juguetes.html",
        juguetes=juguetes,
        title="Lista de juguetes",
        current_user=current_user,
    )


def create_juguete():
    return render_template(
        "create_juguete.html", title="Crear Juguete", current_user=current_user
    )


# La función `update_libro` recibe un libro
# y renderiza el template `update_libro.html`
def update_juguete(juguete):
    return render_template(
        "update_juguete.html",
        title="Editar Juguete",
        juguete=juguete,
        current_user=current_user,
    )
