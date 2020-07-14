#! -* coding: utf-8 -*-

import logging

from flask import Flask
# from base import SanboxBlueprint


level = logging.getLevelName(level="INFO")
logging.basicConfig(
    level=level,
    format="%(asctime)s [%(name)s] %(funcName)s[line:%(lineno)d] %(levelname)-7s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def create_app():

    app = Flask(__name__)

    from admin.blueprint import admin_bp
    app.register_blueprint(admin_bp)

    from cve.blueprint import cve_bp
    app.register_blueprint(cve_bp)

    logging.info("Start web service........................")
    return app
    # app.run()


# if __name__ == '__main__':
#     create_app()

