from pydantic import BaseModel, EmailStr
from typing import List


class BaseContacts:
    name: str
    lastname: str
    phone_number: str
    email: EmailStr
    foto: str


class Group(BaseModel):
    group_name: str
    contacts: List[dict]


class Contacts(BaseModel, BaseContacts):
    relationship: str = None


class User(BaseModel, BaseContacts):
    user: str
    password: str
    contacts: List[Contacts]
    groups: List[Group]
