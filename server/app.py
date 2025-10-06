from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Scientist, Planet, Mission
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route('/')
def home():
    return ''

class Scientists(Resource):
    def get(self):
        scientists = [scientist.to_dict(only=('id', 'name', 'field_of_study')) for scientist in Scientist.query.all()]
        return make_response(scientists, 200)

    def post(self):
        data = request.get_json()
        try:
            scientist = Scientist(name=data['name'], field_of_study=data['field_of_study'])
            db.session.add(scientist)
            db.session.commit()
            return make_response(scientist.to_dict(only=('id', 'name', 'field_of_study', 'missions')), 201)
        except ValueError as e:
            return make_response({'errors': ['validation errors']}, 400)

class ScientistById(Resource):
    def get(self, id):
        scientist = db.session.get(Scientist, id)
        if not scientist:
            return make_response({'error': 'Scientist not found'}, 404)
        return make_response(scientist.to_dict(), 200)

    def patch(self, id):
        scientist = db.session.get(Scientist, id)
        if not scientist:
            return make_response({'error': 'Scientist not found'}, 404)
        data = request.get_json()
        try:
            for key, value in data.items():
                setattr(scientist, key, value)
            db.session.commit()
            return make_response(scientist.to_dict(only=('id', 'name', 'field_of_study', 'missions')), 202)
        except ValueError as e:
            return make_response({'errors': ['validation errors']}, 400)

    def delete(self, id):
        scientist = db.session.get(Scientist, id)
        if not scientist:
            return make_response({'error': 'Scientist not found'}, 404)
        db.session.delete(scientist)
        db.session.commit()
        return make_response({}, 204)

class Planets(Resource):
    def get(self):
        planets = [planet.to_dict(only=('id', 'name', 'distance_from_earth', 'nearest_star')) for planet in Planet.query.all()]
        return make_response(planets, 200)

class Missions(Resource):
    def post(self):
        data = request.get_json()
        try:
            mission = Mission(
                name=data['name'],
                scientist_id=data['scientist_id'],
                planet_id=data['planet_id']
            )
            db.session.add(mission)
            db.session.commit()
            return make_response(mission.to_dict(), 201)
        except ValueError as e:
            return make_response({'errors': ['validation errors']}, 400)

api.add_resource(Scientists, '/scientists')
api.add_resource(ScientistById, '/scientists/<int:id>')
api.add_resource(Planets, '/planets')
api.add_resource(Missions, '/missions')

if __name__ == '__main__':
    app.run(port=5555, debug=True)