from repository.sqlalchemy_repository import *
from repository.unit_of_work import UnitOfWork

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
# try:
#     with UnitOfWork() as unit_of_work:
#         repo = SQLAlchemyUserRepository(unit_of_work.session)
#         likes = repo.get_likes(2)
#         for like in likes:
#             print(like.dict())
#
# except UserAlreadyExistsException as e:
#     print(e.message)
# except UserNotFoundException as e:
#     print(e.message)

# with UnitOfWork() as unit_of_work:
#     content_repo = SQLAlchemyContentRepository(unit_of_work.session)
#     content = content_repo.add(
#         text='Здравствуй, Васька',
#         content_type=ContentType.COMMENT,
#         user_id=1,
#         #parent_id=2
#     )
#
#     #content_repo.delete(1)
#
#
#     unit_of_work.commit()

with UnitOfWork() as unit_of_work:
    repo = SQLAlchemyLikeRepository(unit_of_work.session)

    repo.add(1, 2)

    unit_of_work.commit()
