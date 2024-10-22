from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)

    favorites=db.relationship("Favorite", back_populates="user", lazy=True)

    def __repr__(self):
        return '<User %r>' % self.name
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
    def serialize_favorites(self):
        return [favorite.serialize() for favorite in self.favorites]

        

class Favorite(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'))
    user=db.relationship("User")

    people_id =db.Column(db.Integer, db.ForeignKey('people.id'))
    people=db.relationship("People")

    planet_id =db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet=db.relationship("Planet")

    def __repr__(self):
        return '<Favorite %r>' % self.id
        
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize() if self.user is not None else "",
            "people": self.people.serialize() if self.people is not None else "",
            "planets": self.planet.serialize() if self.planet is not None else "",

        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.String(80), unique=False, nullable=False)
    occupation = db.Column(db.String(100), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name
        

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "occupation": self.occupation,
            "address": self.address
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    galaxy = db.Column(db.String(100), unique=False, nullable=False)
    type_of_inhabitant = db.Column(db.String(80), unique=False, nullable=False)
    inhabitant_height= db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name
        

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "galaxy": self.galaxy,
            "type_of_inhabitant": self.type_of_inhabitant,
            "inhabitant_height": self.inhabitant_height
        }