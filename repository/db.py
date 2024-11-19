from core.config import DB_URL

from sqlalchemy import create_engine
from sqlalchemy import event

engine = create_engine(DB_URL,
                       echo=True
                       )


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Base.metadata.create_all(engine)
