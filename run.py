from app import create_app
from app.db import init_db

init_db()  # ✅ initializes DB on first run
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
