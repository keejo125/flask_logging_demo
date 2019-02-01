# -*- coding: utf-8 -*-
# author：zhengk
from . import module
from .functions import record
import logging

logger = logging.getLogger(__name__)


@module.route('/test1', methods=['GET'])
def test_own_logger():
    logger.info('logged by flask.app.module')
    return 'logged by logging from module.functions'


@module.route('/test2', methods=['GET'])
def test_own_logger_function():
    record()
    return 'logged by logging from module.functions'


