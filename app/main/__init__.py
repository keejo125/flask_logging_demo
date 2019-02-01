# -*- coding: utf-8 -*-
# author：zhengk
from flask import Blueprint

main = Blueprint('main',__name__)

from . import views
