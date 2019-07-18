"""Init Form service."""
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_cors import CORS

APP = Flask(__name__)

CORS(APP)

API = Api(APP, catch_all_404s=True)

MA = Marshmallow(APP)

from form_service.views import view_form  # pylint: disable=wrong-import-position
