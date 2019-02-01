# coding;utf-8
# author：zhengk
from flask import Flask
from config import config
import logstash
import logging


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_logging(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .module import module as module_blueprint
    app.register_blueprint(module_blueprint, url_prefix='/module')

    return app


def register_logging(app):
    app.logger.name = 'app'

    # logstash_handler
    stashHandler = logstash.LogstashHandler(app.config.get('ELK_HOST'), app.config.get('ELK_PORT'))
    app.logger.addHandler(stashHandler)

    # socket_handler
    socketHandler = logging.handlers.SocketHandler('localhost', logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    app.logger.addHandler(socketHandler)
    print(app.logger.name)

    # set own root logger
    rootLogger = logging.getLogger(__name__)
    rootLogger.setLevel(logging.DEBUG)
    socketHandler = logging.handlers.SocketHandler('localhost',logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    rootLogger.addHandler(socketHandler)
    rootLogger.setLevel(logging.DEBUG)
