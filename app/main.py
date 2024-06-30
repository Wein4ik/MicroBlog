from app.exceptions import UserAlreadyExistsException
from db import engine
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
try:
    with UnitOfWork() as unit_of_work:
        repo = SQLAlchemyUserRepository(unit_of_work.session)

        user = repo.add(username='Xrust1k')
        unit_of_work.commit()
        print(user.dict())
except UserAlreadyExistsException as e:
    print(e.message)
