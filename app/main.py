from db import engine
from models import *

from sqlalchemy import and_
from sqlalchemy.orm import Session

# with Session(engine) as session:
#     like = session.query(Like).filter_by(id=1).first()
#     print(f'Лайк поставил {like.user.username} под постом пользователя {like.content.user.username}')


with Session(engine) as session:
    like1 = Like(user_id=1, content_id=2)
    like2 = Like(user_id=2, content_id=1)
    session.add_all([like1, like2])
    session.commit()
