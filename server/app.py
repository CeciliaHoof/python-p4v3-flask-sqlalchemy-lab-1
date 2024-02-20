# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def earthquake(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()
    if not earthquake:
        earthquake_response = {
            "message": f"Earthquake {id} not found."
        }
        response = make_response(
        jsonify(earthquake_response),
        404
    )
    else:
        earthquake_response = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        response = make_response(
            jsonify(earthquake_response),
            200
        )
    return response

@app.route('/earthquakes/magnitude/<float:magnitude>')
def min_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    count = len(earthquakes)
    quakes = []
    for earthquake in earthquakes:
        res = {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        quakes.append(res)
    
    earthquake_response = {
        "count": count,
        "quakes": quakes
    }

    response = make_response(jsonify(earthquake_response), 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
