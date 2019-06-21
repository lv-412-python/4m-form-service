"""Database connection."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from form_service import APP
from form_service.config.dev_config import DevConfiguration


APP.config.from_object(DevConfiguration)
DB = SQLAlchemy(APP)


MIGRATE = Migrate(APP, DB)
