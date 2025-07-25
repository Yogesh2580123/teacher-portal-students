from flask import Flask
from flask_login import LoginManager
from app.db import init_db
from app.models import Student  # Your user model


login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'

    init_db()  # ✅ Initializes your SQLite database and tables
        # Initialize login manager with app
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Change this to your actual login route endpoint

    # Register your blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app

@login_manager.user_loader
def load_user(user_id):
    return Student.get(user_id)  # Your method to get user by ID