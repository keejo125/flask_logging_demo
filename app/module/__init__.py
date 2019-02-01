# -*- coding: utf-8 -*-
# author：zhengk
from flask import Blueprint

module = Blueprint('module',__name__)

from . import views
