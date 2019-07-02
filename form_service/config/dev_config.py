"""Configuration for development."""
from form_service.config.base_config import Configuration


class DevConfiguration(Configuration):
    """Class with development config."""
    DEVELOPMENT = True
    DEBUG = True
