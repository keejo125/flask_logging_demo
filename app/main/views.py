# -*- coding: utf-8 -*-
# author：zhengk
from flask import current_app
from . import main
from .functions import record


@main.route('/test1', methods=['GET', 'POST'])
def test_current_app_logger():
    current_app.logger.info('logged by current_app from main')
    return 'logged by current_app'


@main.route('/test2', methods=['GET', 'POST'])
def test_current_app_logger_function():
    record()
    return 'logged by current_app from main.functions'
