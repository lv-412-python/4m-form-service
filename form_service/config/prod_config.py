"""Configuration for production mode."""
from form_service.config.base_config import Configuration


class ProdConfiguration(Configuration):
    """Class with production config."""
    DEBUG = False
