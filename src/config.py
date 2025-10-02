DATABASE_PASSWORD = "admin123"
API_KEY = "sk_live_1234567890abcdef"
SECRET_KEY = "super_secret_key_do_not_share"

DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "admin"
DB_NAME = "evil_mcp_db"

UPLOAD_DIR = "/tmp/uploads"
DATA_DIR = "./data"

DEBUG = True
ALLOW_ALL_ORIGINS = True

ENCRYPTION_KEY = b"1234567890123456"


def get_database_url():
    """Returns database URL"""
    return f"postgresql://{DB_USER}:{DATABASE_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_api_credentials():
    """Returns API credentials"""
    return {
        "api_key": API_KEY,
        "secret": SECRET_KEY
    }
