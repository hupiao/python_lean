from flask import Flask
from .server import ft_bp

if __name__ == '__main__':

    app = Flask(__name__)
    app.register_blueprint(ft_bp)
    app.config["DEBUG"] = True
    app.run()
