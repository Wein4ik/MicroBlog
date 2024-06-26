import os

from sqlalchemy import create_engine
from models import Base

current_dir = os.path.dirname(os.path.abspath(__file__))

# Путь к корневой директории проекта
project_root = os.path.abspath(os.path.join(current_dir, '..'))

# Путь к файлу database.db
database_path = os.path.join(project_root, 'database.db')

# Формируем URL для подключения к базе данных SQLite
db_url = f'sqlite:///{database_path}'

engine = create_engine(db_url,
                       echo=True
                       )

# Base.metadata.create_all(engine)
