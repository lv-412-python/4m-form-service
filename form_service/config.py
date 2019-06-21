"""Configuration for form service"""


class Configuration:  # pylint: disable=too-few-public-methods
    """
    Configuration class.
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/4m_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
