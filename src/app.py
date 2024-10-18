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
from models import db, User,Favorites, People, Planets
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
    results=User.query.all()
    if results==[]:
        return jsonify({"Message": "Not found"}),404
    response=[ item.serialize() for item in results ]
    return jsonify(response), 200    

@app.route('/user/<int:user_id>', methods=['GET'])
def list_user(user_id):
    results=User.query.filter_by(id=user_id).first()
    if results is None:
        return jsonify({"Message": "Not found"}),404
    return jsonify(results.serialize()), 200

@app.route('/favorites', methods=['GET'])
def favorites_all():
    results=Favorites.query.all()
    if results==[]:
        return jsonify({"Message": "Not found"}),404
    response=[ item.serialize() for item in results ]
    return jsonify(response),200

@app.route('/people', methods=['GET'])
def people_all():
    results=People.query.all()
    if results==[]:
        return jsonify({"Message": "Not found"}),404
    response=[ item.serialize() for item in results ]
    return jsonify(response), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def list_people(people_id):
    results=People.query.filter_by(id=people_id).first()
    if results is None:
        return jsonify({"Message": "Not found"}),404
    return jsonify(results.serialize()), 200

@app.route('/planets', methods=['GET'])
def planets_all():
    results=Planets.query.all()
    if results==[]:
        return jsonify({"Message": "Not found"}),404
    response=[ item.serialize() for item in results ]
    return jsonify(response), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def list_planet(planet_id):
    results=Planets.query.filter_by(id=planet_id).first()
    if results is None:
        return jsonify({"Message": "Not found"}),404
    return jsonify(results.serialize()), 200


@app.route('/people', methods=['POST'])
def add_new_people():
    request_body = request.get_json(force=True)
    new_people=People(
        name=request_body["name"],
        age=request_body["age"],
        occupation=request_body["occupation"],
        address=request_body["address"],
        is_active=request_body["is_active"]
    )
    db.session.add(new_people)
    db.session.commit()
    return jsonify({"message": "People create"}), 201

@app.route('/planet', methods=['POST'])
def add_new_planet():
    request_body = request.get_json(force=True)
    new_planet=Planets(
        name=request_body["name"],
        galaxy=request_body["galaxy"],
        type_of_inhabitant=request_body["type_of_inhabitant"],
        inhabitant_height=request_body["inhabitant_height"],
        is_active=request_body["is_active"]
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"message": "Planet create"}), 201

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    results=People.query.filter_by(id=people_id).first()
    if results is None:
        return jsonify({"Message": "Not found"}),404
    db.session.delete(results)
    db.session.commit()
    return jsonify({"message": "People delete"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
