"""A Device Registry API intended for use with Smart Home devices to provide
a central system for saving and getting device data."""

import shelve, markdown
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("devies.db")
    return db

@app.teardown_appcontext
def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    """Present the README"""
    with open('README.md') as readme_file:
        content = readme_file.read()
        return markdown.markdown(content)

class DeviceList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        devices = []

        for key in keys:
            devices.append(shelf[key])

        return {'message': 'Success', 'data': devices}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('device_type', required=True)
        parser.add_argument('controller_gateway', required=True)

        args = parser.parse_args()

        shelf = get_db()
        shelf[args['identifier']] = args

        return {'message': 'Device registered', 'data': args}, 201

class Device(Resource):
    def get(self, identifier):
        shelf = get_db()

        if not identifier in shelf:
            return {'message': 'Device not found', 'data': {}}, 404
  
        return {'message': 'Device found', 'data': shelf[identifier]}, 200
 
    def delete(self, identifier):
        shelf = get_db()

        if not identifier in shelf:
            return {'message': 'Device not found', 'data': {}}, 404

        del shelf[identifier]
        return '', 204

api.add_resource(DeviceList, '/devices')
api.add_resource(Device, '/devices/<string:identifier>')

if __name__ == "__main__":
    app.run(debug=True)
