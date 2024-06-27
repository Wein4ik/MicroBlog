import os

current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(current_dir, '..'))

DATABASE_PATH = os.path.join(PROJECT_ROOT, 'database.db')

DB_URL = f'sqlite:///{DATABASE_PATH}'
