from app.config import DB_URL

from sqlalchemy import create_engine

engine = create_engine(DB_URL,
                       echo=True
                       )

# Base.metadata.create_all(engine)
