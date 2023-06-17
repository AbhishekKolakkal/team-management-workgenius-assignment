from flask import Flask
from .models import db
from .routes import ma as ma_bp
from .database import db
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()



    app.register_blueprint(ma_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
