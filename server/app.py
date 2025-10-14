
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Configuration de l’application Flask
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importer le modèle après avoir initialisé db
from models import Message


# =======================
# ROUTES CRUD
# =======================
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([msg.to_dict() for msg in messages]), 200


@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    if not data or 'body' not in data or 'username' not in data:
        return jsonify({'error': 'Champs manquants'}), 400

    new_message = Message(
        body=data['body'],
        username=data['username']
    )
    
    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_dict()), 201


@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message introuvable'}), 404

    data = request.get_json()
    if 'body' in data:
        message.body = data['body']
    db.session.commit()
    return jsonify(message.to_dict()), 200


@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message introuvable'}), 404

    db.session.delete(message)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(port=5000, debug=True)