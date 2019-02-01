# -*- coding: utf-8 -*-
# author：zhengk
from flask import current_app


def record():
    current_app.logger.info('logged by current_app of functions')
    return True
