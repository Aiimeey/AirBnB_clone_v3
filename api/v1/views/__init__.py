#!/usr/bin/python3
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# This wildcard import is intentional to import the views module
# Don't worry about PEP8 warnings for this file
from api.v1.views.index import *
