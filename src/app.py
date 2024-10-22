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
from models import db, User,Favorite, People, Planet
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

@app.route('/users', methods=['GET'])
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

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def favorites_all(user_id):
    user=User.query.get(user_id)
    if user is None:
        return jsonify({"Message": "Not found"}),404
    return jsonify(user.serialize_favorites()),200

@app.route('/people', methods=['GET'])
def people_all():
    results=People.query.all()
    if results==[]:
        return jsonify({"Message": "Not found"}),404
    response=[ item.serialize() for item in results ]
    return jsonify(response), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def list_people(people_id):
    results=People.query.get(people_id)
    if results is None:
        return jsonify({"Message": "Not found"}),404
    return jsonify(results.serialize()), 200

@app.route('/planets', methods=['GET'])
def planets_all():
    results=Planet.query.all()
    if results==[]:
        return jsonify({"Message": "Not found"}),404
    response=[ item.serialize() for item in results ]
    return jsonify(response), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def list_planet(planet_id):
    results=Planet.query.get(planet_id)
    if results is None:
        return jsonify({"Message": "Not found"}),404
    return jsonify(results.serialize()), 200


@app.route('/favorite/user/<int:user_id>/people/<int:people_id>', methods=['POST'])
def add_new_favorite_people(user_id, people_id):
    new_favorite=Favorite(
        user_id=user_id,
        people_id=people_id
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "Favorite created"}), 201

@app.route('/favorite/user/<int:user_id>/people/<int:people_id>', methods=['DELETE'])
def delete_one_favorite_people(user_id, people_id):
    favorite=Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite is None:
        return jsonify({"Message": "Not found"}),404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted"}), 201


@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_new_favorite_planet(user_id, planet_id):
    new_favorite=Favorite(
        user_id=user_id,
        planet_id=planet_id
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"message": "Favorite created"}), 201

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['DELETE'])
def delete_one_favorite_planet(user_id, planet_id):
    favorite=Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({"Message": "Not found"}),404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted"}), 201





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
