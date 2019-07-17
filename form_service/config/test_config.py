"""Configuration for testing mode."""
from form_service.config.base_config import Configuration


class TestConfiguration(Configuration):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/4m_forms_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
