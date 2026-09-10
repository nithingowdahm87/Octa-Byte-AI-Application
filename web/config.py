import os

_db_user = os.environ.get('DB_USER', '')
if not _db_user and 'POSTGRES_USER_FILE' in os.environ:
    with open(os.environ['POSTGRES_USER_FILE']) as f:
        _db_user = f.read().strip()

_db_pass = os.environ.get('DB_PASS', '')
if not _db_pass and 'POSTGRES_PASSWORD_FILE' in os.environ:
    with open(os.environ['POSTGRES_PASSWORD_FILE']) as f:
        _db_pass = f.read().strip()

_db_host = os.environ.get('DB_HOST', 'postgres')
_db_name = os.environ.get('POSTGRES_DB', os.environ.get('DB_NAME', 'db'))
_db_port = os.environ.get('DATABASE_PORT', os.environ.get('DB_PORT', '5432'))

class BaseConfig(object):
    DEBUG = os.environ.get('DEBUG', 'False') == 'True'
    DB_NAME = _db_name
    DB_USER = _db_user
    DB_PASS = _db_pass
    DB_PORT = _db_port
    DB_HOST = _db_host
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
