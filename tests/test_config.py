import os
import pytest

from config.config import config_by_name


basedir = os.path.abspath(os.path.dirname(__name__))

@pytest.mark.config
def test_production_config(app):
    '''Assert that the `prod` configurations defined in config.py have correct values'''
    app.config.from_object(config_by_name['prod'])
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('PROD_DATABASE_URL') or app.config['SQLALCHEMY_DATABASE_URI'] is None


@pytest.mark.config
def test_development_config(app):
    '''Assert that the `dev` configurations defined in config.py have correct values'''
    app.config.from_object(config_by_name['dev'])
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DEV_DATABASE_URL') or f"sqlite:///{os.path.join(basedir, 'data.db')}"


@pytest.mark.config
def test_testing_config(app):
    '''Assert that the `test` configurations defined in config.py have correct values'''
    app.config.from_object(config_by_name['test'])
    assert not app.config['DEBUG']
    assert app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DEV_DATABASE_URL') or f"sqlite:///{os.path.join(basedir, 'test-data.db')}"


