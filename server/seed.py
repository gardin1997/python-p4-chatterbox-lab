from app import app, db
from models import Message

with app.app_context():
    db.drop_all()
    db.create_all()

    messages = [
        Message(body="Salut tout le monde !", username="Gardin"),
        Message(body="Bienvenue sur Chatterbox 💬", username="Admin"),
    ]

    db.session.add_all(messages)
    db.session.commit()

    print("Base de données initialisée avec succès !")