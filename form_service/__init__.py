"""Init Form service."""
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api

APP = Flask(__name__)

API = Api(APP, catch_all_404s=True)

MA = Marshmallow(APP)

from form_service.views import view_form  # pylint: disable=wrong-import-position
