import os
import pytest
from unittest import mock

def test_missing_database_host_uses_db_in_local():
    with mock.patch.dict(os.environ, {"DEBUG": "True"}, clear=True):
        import config
        import importlib
        importlib.reload(config)
        assert config.BaseConfig.DATABASE_HOST == 'db'

def test_missing_database_host_fails_in_production():
    with mock.patch.dict(os.environ, {"DATABASE_PASSWORD": "pass"}, clear=True):
        import config
        import importlib
        with pytest.raises(ValueError, match="DATABASE_HOST is missing."):
            importlib.reload(config)

def test_database_password_required_in_production():
    with mock.patch.dict(os.environ, {"DATABASE_HOST": "db"}, clear=True):
        import config
        import importlib
        with pytest.raises(ValueError, match="DATABASE_PASSWORD is required in staging/production."):
            importlib.reload(config)

def test_database_host_produces_uri_using_db():
    with mock.patch.dict(os.environ, {"DATABASE_HOST": "db", "DATABASE_PASSWORD": "pass"}, clear=True):
        import config
        import importlib
        importlib.reload(config)
        assert 'postgresql://postgres:pass@db:5432/postgres' == config.BaseConfig.SQLALCHEMY_DATABASE_URI

def test_passwords_with_special_characters_handled():
    with mock.patch.dict(os.environ, {"DATABASE_HOST": "db", "DATABASE_PASSWORD": "my@!password?"}, clear=True):
        import config
        import importlib
        importlib.reload(config)
        assert 'my%40%21password%3F' in config.BaseConfig.SQLALCHEMY_DATABASE_URI

def test_ready_health_check_handles_unavailable_db():
    with mock.patch.dict(os.environ, {"DATABASE_HOST": "invalid_host", "DATABASE_PASSWORD": "pass", "DEBUG": "False"}, clear=True):
        import config
        import importlib
        importlib.reload(config)
        
        import app
        importlib.reload(app)
        
        client = app.app.test_client()
        response = client.get('/ready')
        assert response.status_code == 503
        assert response.json == {"status": "not ready"}
