import os
from flask import Flask
from .routes.api_endpoints import bp as locker_bp
from src.locker_finder.db.database import create_db_and_tables

app = Flask(__name__, root_path=os.path.dirname(__file__))
app.register_blueprint(locker_bp)

create_db_and_tables()

if __name__ == '__main__':
    app.run(debug=True)