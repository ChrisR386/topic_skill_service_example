from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    # Stelle sicher, dass Username, Passwort und DB-Name passen
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:secret@localhost:5432/topicdb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)