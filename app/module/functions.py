# -*- coding: utf-8 -*-
# author：zhengk
import logging

logger = logging.getLogger(__name__)


def record():
    logger.info('logged by logging module of functions')
    return True
