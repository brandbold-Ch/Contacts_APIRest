from Models.models import Contacts, Group, User
from abc import ABC, abstractmethod


class MethodsContrat(ABC):

    @abstractmethod
    async def create_user(self, user: User) -> list:
        pass

    @abstractmethod
    async def login(self, user: str, password: str) -> bool:
        pass

    @abstractmethod
    async def get_users(self) -> list:
        pass

    @abstractmethod
    async def get_user(self, _id_user: str) -> list:
        pass

    @abstractmethod
    async def edit_user_context(self, _id_user: str, user: User) -> list:
        pass

    @abstractmethod
    async def get_contacts(self, _id_user: str) -> list:
        pass

    @abstractmethod
    async def get_contact(self, _id_user: str, contact_name: str) -> list:
        pass

    @abstractmethod
    async def set_contact(self, _id_context: str, contact: Contacts) -> list:
        pass

    @abstractmethod
    async def edit_contact(self, _id: str, contact_name: str, contact: Contacts) -> list:
        pass

    @abstractmethod
    async def del_contact(self, _id_user: str, contact_name: str) -> list:
        pass

    @abstractmethod
    async def get_groups(self, _id_context: str) -> list:
        pass

    @abstractmethod
    async def get_group(self, _id_user: str, group_name: str) -> list:
        pass

    @abstractmethod
    async def set_group(self, _id_user, group: Group) -> list:
        pass

    @abstractmethod
    async def del_group(self, name: str, group_name: str) -> list:
        pass

    @abstractmethod
    async def add_contact_to_group(self, _id_context, contact_name: str, group_name: str) -> list:
        pass
