"""Configuration for form service."""


class Configuration:
    """Base configuration class."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = \
        'postgres://kkxeulhg:bq35nWtkFTw4Ef04or0u74pspv54ntR2@balarama.db.elephantsql.com:5432/kkxeulhg'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
