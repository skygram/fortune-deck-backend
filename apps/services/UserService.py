from __future__ import absolute_import, division, print_function, unicode_literals

from apps.repositories.UserRepository import IUserRepository
from apps.model.User import UserModel

class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get_new_obj(self) -> UserModel:
        return UserModel()

    def get_bots(self) -> list:
        return self.user_repository.get_list()

    def find_by_id(self, uid: str) -> UserModel:
        return self.user_repository.find_by_id(uid)

    def add(self, user: UserModel):
        self.user_repository.save(user)

    def edit(self, user: UserModel):
        return self.user_repository.save(user)

    # def fit(self, user: str):

    #     user = self.find_by_id(user)
    #     self.edit(user)

    #     #async异步通知更新
