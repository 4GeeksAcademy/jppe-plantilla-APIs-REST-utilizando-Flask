"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personajes, Planetas,Favoritos_Planetas,Favoritos_P
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.serialize()), 200


@app.route('/Personajes', methods=['GET'])
def get_personajes():
    todos_personajes = Personajes.query.all()
    print(todos_personajes)
    results = list(map(lambda personajes: personajes.serialize(), Personajes))
    print(results)

    response_body = {
        "msg": "Hello, this is your GET /Personajes response "
    }

    return jsonify(response_body), 200

@app.route('/Personajes/<int:personajes_id>', methods=['GET'])
def get_personaje(personajes_id):
    personaje = Personajes.query.filter_by(id=personajes_id).first()
    return jsonify(personaje.serialize()), 200

@app.route('/Planetas', methods=['GET'])
def han_hello():

    response_body = {
        "msg": "Hello, this is your GET /Planetas response "
    }

    return jsonify(response_body), 200

@app.route('/Planetas/<int:planetas_id>', methods=['GET'])
def get_planet(planetas_id):
    planetas = Planetas.query.filter_by(id=planetas_id).first()
    return jsonify(planetas.serialize()), 200

@app.route('/Vehiculos', methods=['GET'])
def handle_hllo():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/Favoritos_P', methods=['GET'])
def get_favoritos_p():

    received_user_id = request.json.get('id')
    results = Favoritos_P.query.filter_by(user_id = received_user_id).all()
    Favoritos_P_serialized = list(map(lambda element: element.serialize(), results))

    return jsonify({'favoritos_P': Favoritos_P_serialized}), 200


@app.route('/Favoritos_Planetas', methods=['GET'])
def get_favoritos_planetas():
    received_user_id = request.json.get('id')
    results = Favoritos_Planetas.query.filter_by(user_id = received_user_id).all()
    favoritos_Planetas_serialized = list(map(lambda element: element.serialize(), results))

    return jsonify({'Favoritos_Planetas': favoritos_Planetas_serialized}), 200


# TODOS LOS POST

@app.route('/Personajes', methods=['POST'])
def crear_personaje():
    # Leer los datos que envia solicitud (body)
    data = request.json
    if not "name" in data:
        return jsonify("Se debe enviar el character"), 400
    if data["name"] == "":
        return jsonify("El character no debe ser vacio"), 400
    # Crear character nuevo
    charact = Personajes(**data)
    db.session.add(charact)
    db.session.commit()

    response_body = {
        "msg": "CREAR LOS USUARIOS "
    }

    return jsonify(response_body), 200



@app.route('/Planetas', methods=['POST'])
def crear_planeta():
    # Leer los datos que envia solicitud (body)
    data = request.json
    if not "diameter" in data:
        return jsonify("Se debe enviar el planet"), 400
    if data["diameter"] == "":
        return jsonify("El planet no debe ser vacio"), 400
    # Crear planet nuevo
    planet = Planetas(**data)
    db.session.add(planet)
    db.session.commit()

    response_body = {
        "msg": "CREAR LOS PLANETAS "
    }

    return jsonify(response_body), 200



@app.route('/favorite/Planetas/<int:planeta_id>', methods=['POST'])
def add_fav_planetas(planetas_id):
            user_id = request.json.get('user_id')
            existing_favorite = Favoritos_Planetas.query.filter_by(user_id=user_id, planeta_id=planeta_id).first()            
            if existing_favorite:
                return jsonify({"msg": "Personaje favorio del usuario"}), 400            
            planeta = Planetas.query.get(planetas_id)
            if not planeta:
                return jsonify({"msg": "Planeta no existe"}), 404 
            # Crear nuevo planeta favorito          
            new_favorite = Favoritos_Planetas(user_id=user_id, planeta_id=planeta_id)
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify({"msg": "Planeta establecido como favorito"}), 200



@app.route('/favorite/Personajes/<int:personaje_id>', methods=['POST'])
def add_fav_character(personaje_id):
    user_id = request.json.get('user_id')
    
    existing_favorite = Favoritos_P.query.filter_by(user_id=user_id, personaje_id=personaje_id).first()
    if existing_favorite:
        return jsonify({"msg": "Personaje favorito del usuario"}), 400
    
    personaje = Personajes.query.get(personaje_id)
    if not personaje:
        return jsonify({"msg": "Personaje no existe"}), 404
    # Crear nuevo personaje favorito  
    new_favorite = Favoritos_P(user_id=user_id, personaje_id=personaje_id)
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify({"msg": "Personaje establecido como favorito"}), 200


#Delete

@app.route('/Personajes/<int:id>', methods=['DELETE'])
def delete_Persnaje(id):
    # Buscar el personaje por su ID en la base de datos
    personaje = Personajes.query.get(id)

    # Si no se encuentra el personaje, devuelve un error 404
    if personaje is None:
        return jsonify("Personaje no encontrado"), 404

    # Eliminar el personaje de la base de datos
    db.session.delete(personaje)
    db.session.commit()

    # Devolver una respuesta exitosa
    return jsonify({"msg": "Personaje eliminado exitosamente"}), 200



@app.route('/Planetas/<int:id>', methods=['DELETE'])
def delete_planetas(id):
    # Buscar el personaje por su ID en la base de datos
    planeta = Planetas.query.get(id)

    # Si no se encuentra el personaje, devuelve un error 404
    if planeta is None:
        return jsonify("Planeta no encontrado"), 404

    # Eliminar el personaje de la base de datos
    db.session.delete(planeta)
    db.session.commit()

    # Devolver una respuesta exitosa
    return jsonify({"msg": "Personaje eliminado exitosamente"}), 200



@app.route('/favorite/Planetas/<int:planetas_id>', methods=['DELETE'])
def delete_one_fav_planet(planeta_id):

    # user_id = request.json.get('user_id')  # Obtener user_id del cuerpo de la solicitud
    # print (planet_id, user_id)
    # return jsonify({"msg": "Fav Planet deleted successfully"}), 200
    
        user_id = request.json.get('user_id')  # Obtener user_id del cuerpo de la solicitud
        print (planeta_id, user_id)
        existing_favorite = Favoritos_Planetas.query.filter_by(user_id=user_id, planeta_id=planeta_id).first()
        if existing_favorite:
            db.session.delete(existing_favorite)  # Eliminar la fila existente
            db.session.commit()
            return jsonify({"msg": "Planeta favorito borrado"}), 200
        planeta = Planetas.query.get(planetas_id)
        if not planeta:
            return jsonify({"msg": "planeta favorito no existe"}), 404
        

        
@app.route('/favorite/Personajes/<int:personajes_id>', methods=['DELETE'])
def delete_one_fav_character(personaje_id):
    user_id = request.json.get('user_id')  # Obtener user_id del cuerpo de la solicitud
    existing_favorite = Favoritos_P.query.filter_by(user_id=user_id, personaje_id=personaje_id).first()
    
    if existing_favorite:
        db.session.delete(existing_favorite)  # Eliminar la fila existente
        db.session.commit()
        return jsonify({"msg": "Personaje favorito borrado"}), 200
    
    personaje = Personajes.query.get(personaje_id)
    if not personaje:
        return jsonify({"msg": "Personaje favorito no existe"}), 404




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
