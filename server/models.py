from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    field_of_study = db.Column(db.String, nullable=False)

    # Relationships
    missions = db.relationship('Mission', back_populates='scientist', cascade='all, delete-orphan')

    # Serialization rules to prevent infinite recursion
    serialize_rules = ('-missions.scientist',)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Scientist must have a name')
        return name

    @validates('field_of_study')
    def validate_field_of_study(self, key, field_of_study):
        if not field_of_study:
            raise ValueError('Scientist must have a field of study')
        return field_of_study

class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    distance_from_earth = db.Column(db.Integer, nullable=False)
    nearest_star = db.Column(db.String, nullable=False)

    # Relationships
    missions = db.relationship('Mission', back_populates='planet', cascade='all, delete-orphan')

    # Serialization rules
    serialize_rules = ('-missions.planet',)

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    # Relationships
    scientist = db.relationship('Scientist', back_populates='missions')
    planet = db.relationship('Planet', back_populates='missions')

    # Serialization rules
    serialize_rules = ('-scientist.missions', '-planet.missions')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Mission must have a name')
        return name

    @validates('scientist_id')
    def validate_scientist_id(self, key, scientist_id):
        if not scientist_id:
            raise ValueError('Mission must have a scientist_id')
        return scientist_id

    @validates('planet_id')
    def validate_planet_id(self, key, planet_id):
        if not planet_id:
            raise ValueError('Mission must have a planet_id')
        return planet_id