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
from models import db, User, Contact
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/contact', methods=['GET'])
def get_contact():

    contacts = Contact.query.all()
    results = list(map(lambda item: item.serialize(),contacts))

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "contacts": results
    }

    return jsonify(response_body), 200


@app.route('/contact', methods=['POST'])
def post_contact():
    body = request.get_json()
    newContact = Contact(full_name= body["full_name"],email = body["email"], address = body["address"],phone = body["phone"])
    db.session.add(newContact)
    db.session.commit()

    response_body = {
        "msg": "Contact added successfuly "
    }

    return jsonify(response_body), 200

@app.route('/contact/<int:contactId>', methods=['GET'])
def get_contact_id(contactId):
    contacts = Contact.query.filter_by(id=contactId)
    results = list(map(lambda item: item.serialize(),contacts))
    print("resultados ",results)
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "contacts": results
    }

    return jsonify(response_body), 200

@app.route('/contact/<int:contactId>', methods=['DELETE'])
def delete_contact(contactId):
    body = request.get_json()
    contactToDelete = Contact.query.filter_by(id=contactId).first()
    print(contactToDelete)
    db.session.delete(contactToDelete)
    db.session.commit()
    response_body = {
        "msg": "Contact deleted"
    }

    return jsonify(response_body), 200

@app.route('/contact/<int:contactId>', methods=['DELETE'])
def update_contact(contactId):
    body = request.get_json()
    contactToDelete = Contact.query.filter_by(id=contactId).first()
    print(contactToDelete)
    db.session.delete(contactToDelete)
    db.session.commit()
    response_body = {
        "msg": "Contact deleted"
    }

    return jsonify(response_body), 200

@app.route('/contact/<int:contactId>', methods=['PUT'])
def update_contact(contactId):
    body = request.get_json()
    contactToDelete = Contact.query.filter_by(id=contactId).first()
    print(contactToDelete)
    db.session.delete(contactToDelete)
    db.session.commit()
    response_body = {
        "msg": "Contact deleted"
    }

    return jsonify(response_body), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
