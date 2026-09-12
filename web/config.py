import os
from sqlalchemy.engine import URL

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
is_local_compose = 'POSTGRES_PASSWORD_FILE' in os.environ or DEBUG

# 1. DATABASE_USERNAME
_db_user = os.environ.get('DATABASE_USERNAME') or os.environ.get('DB_USER')
if not _db_user and 'POSTGRES_USER_FILE' in os.environ:
    with open(os.environ['POSTGRES_USER_FILE']) as f:
        _db_user = f.read().strip()
if not _db_user:
    _db_user = 'postgres'

# 2. DATABASE_PASSWORD
_db_pass = os.environ.get('DATABASE_PASSWORD') or os.environ.get('DB_PASS')
if not _db_pass and 'POSTGRES_PASSWORD_FILE' in os.environ:
    with open(os.environ['POSTGRES_PASSWORD_FILE']) as f:
        _db_pass = f.read().strip()

if not _db_pass and not is_local_compose:
    raise ValueError("DATABASE_PASSWORD is required in staging/production.")

# 3. DATABASE_HOST
_db_host = os.environ.get('DATABASE_HOST') or os.environ.get('DB_HOST')
if not _db_host:
    if is_local_compose:
        _db_host = 'db'
    else:
        raise ValueError("DATABASE_HOST is missing.")

# 4. DATABASE_NAME
_db_name = os.environ.get('DATABASE_NAME') or os.environ.get('DB_NAME') or 'postgres'

# 5. DATABASE_PORT
_db_port = os.environ.get('DATABASE_PORT') or os.environ.get('DB_PORT') or '5432'

class BaseConfig(object):
    DEBUG = DEBUG
    DATABASE_NAME = _db_name
    DATABASE_USERNAME = _db_user
    DATABASE_PASSWORD = _db_pass
    DATABASE_PORT = _db_port
    DATABASE_HOST = _db_host
    
    # Safely build the SQLAlchemy URI using URL.create
    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="postgresql",
        username=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        database=DATABASE_NAME
    ).render_as_string(hide_password=False)
