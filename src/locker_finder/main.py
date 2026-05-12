import os
from flask import Flask
from .routes.api_endpoints import bp as locker_bp

app = Flask(__name__, root_path=os.path.dirname(__file__))
app.register_blueprint(locker_bp)

if __name__ == '__main__':
    app.run(debug=True)