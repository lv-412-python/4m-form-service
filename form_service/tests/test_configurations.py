"""Tests for form service configurations."""
import os
from form_service.config.dev_config import DevConfiguration
from form_service.config.test_config import TestConfiguration
from form_service.config.prod_config import ProdConfiguration


def test_development_config(app):
    """Tests DevConfiguation."""
    app.config.from_object(DevConfiguration)
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
        'DATABASE_URL')


def test_testing_config(app):
    """Tests TestConfiguraion."""
    app.config.from_object(TestConfiguration)
    assert app.config['DEBUG']
    assert app.config['TESTING']
    assert not app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
        'DATABASE_TEST_URL')


def test_production_config(app):
    """Tests ProdConfiguration."""
    app.config.from_object(ProdConfiguration)
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
        'DATABASE_URL')
