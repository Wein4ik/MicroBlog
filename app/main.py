from db import engine
from models import *

from sqlalchemy import and_
from sqlalchemy.orm import Session

# with Session(engine) as session:
#     like = session.query(Like).filter_by(id=1).first()
#     print(f'Лайк поставил {like.user.username} под постом пользователя {like.content.user.username}')


with Session(engine) as session:
    user = User(username='Yulsin')
    session.add(user)
    session.commit()
