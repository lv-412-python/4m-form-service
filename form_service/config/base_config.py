"""Configuration for form service."""
LOCAL_DATABASE = 'postgres://postgres:postgres@localhost:5432/4m_forms'
PG_DOCKER_DATABASE = 'postgres://postgres:mysecretpassword@db:5432/4m_forms'


class Configuration:
    """Base configuration class."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = PG_DOCKER_DATABASE
    SQLALCHEMY_TRACK_MODIFICATIONS = True
