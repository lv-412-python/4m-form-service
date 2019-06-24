"""Init users service"""
from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow

APP = Flask(__name__)

API = Api(APP)

MA = Marshmallow(APP)

from form_service.views import view_form  # pylint: disable=wrong-import-position
