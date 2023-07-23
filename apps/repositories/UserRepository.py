from abc import ABCMeta, abstractclassmethod
from apps.model.User import UserModel


class IUserRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def get_list(self) -> list:
        pass

    @abstractclassmethod
    def find_by_id(self, id: str) -> UserModel:
        pass

    @abstractclassmethod
    def save(self, bot: UserModel):
        pass
