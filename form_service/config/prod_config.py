"""Configuration for production."""
from form_service.config.base_config import Configuration


class ProdConfiguration(Configuration):  # pylint: disable=too-few-public-methods
    """
    Class with production config.
    """
    DEBUG = False
