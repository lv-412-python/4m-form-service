"""Configuration for form service."""


class Configuration:
    """Base configuration class."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:mysecretpassword@172.17.0.3:5432/4m_forms'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
