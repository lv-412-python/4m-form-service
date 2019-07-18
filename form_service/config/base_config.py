"""Configuration for form service."""
LOCAL_DATABASE = 'postgres://postgres:postgres@localhost:5432/4m_forms'
PG_DOCKER_DATABASE = 'postgres://postgres:mysecretpassword@172.17.0.2:5432/4m_forms'


class Configuration:
    """Base configuration class."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = LOCAL_DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = True
