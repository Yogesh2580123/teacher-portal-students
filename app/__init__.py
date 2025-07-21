# from flask import Flask
# from app.db import init_db

# def create_app():
#     app = Flask(__name__)
#     app.secret_key = 'your-secret-key'

#     from app.routes import main
#     app.register_blueprint(main)

#     init_db()
#     return app

from flask import Flask
from app.db import init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'

    from app.routes import main
    app.register_blueprint(main)

    init_db()  # ✅ Initializes your SQLite database and tables
    return app
