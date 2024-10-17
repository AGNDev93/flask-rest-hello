from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

class Favorites(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'))
    user=db.relationship("User")

    people_id =db.Column(db.Integer, db.ForeignKey('people.id'))
    people=db.relationship("People")

    planets_id =db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets=db.relationship("Planets")

    def __repr__(self):
        return '<Favorites %r>' % self.name
        
    def serialize(self):
        return {
            "id": self.id,
            "people": self.people.serialize() if self.people is not None else "",
            "planets": self.planets.serialize() if self.planets is not None else "",
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.String(80), unique=False, nullable=False)
    occupation = db.Column(db.String(100), unique=False, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name
        

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "occupation": self.occupation,
            "address": self.address
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    galaxy = db.Column(db.String(100), unique=False, nullable=False)
    type_of_inhabitant = db.Column(db.String(80), unique=False, nullable=False)
    inhabitant_height= db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name
        

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "galaxy": self.galaxy,
            "type_of_inhabitant": self.type_of_inhabitant,
            "inhabitant_height": self.inhabitant_height
        }