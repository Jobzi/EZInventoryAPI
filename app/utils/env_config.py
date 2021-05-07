import os


class EnvConfig:
    ENV: str = os.environ.get('ENV', 'DEV')
    DB_URL: str = os.environ.get('DB_URL', '').strip()
    TESTING_DB_URL:  str = os.environ.get('TESTING_DB_URL', '').strip()
