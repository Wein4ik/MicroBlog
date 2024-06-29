from db import engine
from models import *
from repository.sqlalchemy_repository import SQLAlchemyUserRepository
from repository.unit_of_work import UnitOfWork

from sqlalchemy.orm import Session

user_repository = SQLAlchemyUserRepository(session=Session(engine))

# users = user_repository.users_list(id=1, username='Yulsin')
#
# print(users)
# for user in users:
#     print(user.username)


# user = user_repository.get_by_id(2)
# if user:
#     print(user.username)
# else:
#     print('Not found')

# user_repository.add(username='Ilyusha')


# user_repository.update(3, )

with UnitOfWork() as unit_of_work:
    repo = SQLAlchemyUserRepository(unit_of_work.session)
    # repo.add(username='Крутой чел ебать')

    delete_user = repo.get_by_username(username='Крутой чел ебать')
    repo.delete(delete_user.id)