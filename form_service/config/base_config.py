"""Configuration for form service"""


class Configuration:  # pylint: disable=too-few-public-methods
    """
    Configuration class.
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = "1ji5$8*@%GUehjw&3WJ@)"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/4m_forms'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
