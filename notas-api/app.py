from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, Usuario, Nota


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return {"mensaje": "API de notas funcionando"}

    @app.route("/register", methods=["POST"])
    def register():
        datos = request.get_json()

        if not datos or not datos.get("email") or not datos.get("password"):
            return jsonify({"error": "email y password son obligatorios"}), 400

        if Usuario.query.filter_by(email=datos["email"]).first():
            return jsonify({"error": "ese email ya está registrado"}), 409

        nuevo_usuario = Usuario(
            email=datos["email"],
            password_hash=generate_password_hash(datos["password"])
        )
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({"mensaje": "usuario creado", "id": nuevo_usuario.id}), 201

    @app.route("/login", methods=["POST"])
    def login():
        datos = request.get_json()

        if not datos or not datos.get("email") or not datos.get("password"):
            return jsonify({"error": "email y password son obligatorios"}), 400

        usuario = Usuario.query.filter_by(email=datos["email"]).first()

        if not usuario or not check_password_hash(usuario.password_hash, datos["password"]):
            return jsonify({"error": "credenciales inválidas"}), 401

        token = create_access_token(identity=str(usuario.id))
        return jsonify({"access_token": token}), 200

    @app.route("/notas", methods=["GET"])
    @jwt_required()
    def listar_notas():
        usuario_id = get_jwt_identity()
        notas = Nota.query.filter_by(usuario_id=usuario_id).all()

        return jsonify([{
            "id": n.id,
            "titulo": n.titulo,
            "contenido": n.contenido,
            "sincronizado": n.sincronizado,
            "actualizado_en": n.actualizado_en.isoformat()
        } for n in notas]), 200

    @app.route("/notas", methods=["POST"])
    @jwt_required()
    def crear_nota():
        usuario_id = get_jwt_identity()
        datos = request.get_json()

        if not datos or not datos.get("titulo"):
            return jsonify({"error": "el título es obligatorio"}), 400

        nueva_nota = Nota(
            titulo=datos["titulo"],
            contenido=datos.get("contenido", ""),
            usuario_id=usuario_id,
            sincronizado=True
        )
        db.session.add(nueva_nota)
        db.session.commit()

        return jsonify({"id": nueva_nota.id, "mensaje": "nota creada"}), 201

    @app.route("/notas/<int:nota_id>", methods=["PUT"])
    @jwt_required()
    def actualizar_nota(nota_id):
        usuario_id = get_jwt_identity()
        nota = Nota.query.filter_by(id=nota_id, usuario_id=usuario_id).first()

        if not nota:
            return jsonify({"error": "nota no encontrada"}), 404

        datos = request.get_json()
        nota.titulo = datos.get("titulo", nota.titulo)
        nota.contenido = datos.get("contenido", nota.contenido)
        nota.sincronizado = True
        db.session.commit()

        return jsonify({"mensaje": "nota actualizada"}), 200

    @app.route("/notas/<int:nota_id>", methods=["DELETE"])
    @jwt_required()
    def eliminar_nota(nota_id):
        usuario_id = get_jwt_identity()
        nota = Nota.query.filter_by(id=nota_id, usuario_id=usuario_id).first()

        if not nota:
            return jsonify({"error": "nota no encontrada"}), 404

        db.session.delete(nota)
        db.session.commit()

        return jsonify({"mensaje": "nota eliminada"}), 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)