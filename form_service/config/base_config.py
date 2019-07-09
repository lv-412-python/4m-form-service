"""Configuration for form service"""


class Configuration:
    """Configuration class."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/4m_forms'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
