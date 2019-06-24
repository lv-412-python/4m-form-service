"""Configuration for development."""
from form_service.config.base_config import Configuration


class DevConfiguration(Configuration):  # pylint: disable=too-few-public-methods
    """
    Class with development config.
    """
    DEVELOPMENT = True
    DEBUG = True
