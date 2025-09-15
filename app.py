from flask import Flask
from db import init_db, db
from routes import bp as api_bp

def create_app():
    app = Flask(__name__)
    init_db(app)
    app.register_blueprint(api_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
