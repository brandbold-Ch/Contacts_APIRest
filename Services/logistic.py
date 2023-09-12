from Models.models import Group, Contacts, User
from Interface.requires import MethodsContrat
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId


class ApiService(MethodsContrat):

    __CLIENT: AsyncIOMotorClient = AsyncIOMotorClient("mongodb://localhost:27017")
    __DB_USERS: str = "Users"

    def __init__(self):
        self.__db_users: AsyncIOMotorClient = ApiService.__database_connect(ApiService.__DB_USERS)

    @staticmethod
    def __database_connect(database: str) -> AsyncIOMotorClient:
        return ApiService.__CLIENT[database]

    async def create_user(self, user: User) -> list:
        try:
            await self.__db_users.users.insert_one(jsonable_encoder(user))
            return [{"message": "Created user"}, 201]
        except Exception as e:
            return [{"alert": str(e)}, 500]

    async def login(self, user: str, password: str) -> bool:
        pass

    async def get_users(self) -> list:
        try:
            list_users: list = []

            async for user in self.__db_users.users.find():
                user["_id"] = str(user["_id"])
                list_users.append(user)
            return [list_users, 200]

        except Exception as e:
            return [{"alert": str(e)}]

    async def get_user(self, _id_user: str) -> list:
        try:
            user: dict = await self.__db_users.users.find_one({"_id": ObjectId(_id_user)})

            if user is not None:
                user["_id"] = str(user["_id"])
                return [[user], 200]
            else:
                return [{"message": "Not found user"}, 404]

        except Exception as e:
            return [{"alert": str(e)}, 500]

    async def edit_user_context(self, _id_user: str, user: User) -> list:
        try:
            user_list: list = await self.get_user(_id_user)

            if user_list[1] == 200:
                await self.__db_users.users.update_one(
                    {"_id": ObjectId(_id_user)},
                    {"$set": jsonable_encoder(user)}
                )
                return [{"message": "Updated user"}, 202]
            else:
                return user_list

        except Exception as e:
            return [{"alert": str(e)}, 500]

    async def get_contacts(self, _id_user: str) -> list:
        try:
            user: list = await self.get_user(_id_user)

            if user[1] == 200:
                return [user[0]["contacts"], 200]
            else:
                return user

        except Exception as e:
            return [{"alert": str(e)}, 500]

    async def get_contact(self, _id_user: str, contact_name: str) -> list:
        try:
            user: list = await self.get_user(_id_user)

            if user[1] == 200:
                contact: dict = await self.__db_users.users.find_one(
                    {"_id": ObjectId(_id_user)},
                    {"contacts": {"$elemMatch": {"name": contact_name.title()}}}
                )

                if len(contact) > 1:
                    return [contact["contacts"][0], 200]
                else:
                    return [{"message": "Not found contact"}, 404]
            else:
                return user

        except Exception as e:
            return [{"alert": str(e)}, 500]

    async def set_contact(self, _id_context: str, contact: Contacts) -> list:
        try:
            user: list = await self.get_user(_id_context)

            if user[1] == 200:
                await self.__db_users.users.update_one(
                    {"_id": ObjectId(_id_context)},
                    {"$push": {"contacts": jsonable_encoder(contact)}}
                )
                return [{"message": "Added contact"}, 201]
            return user

        except Exception as e:
            return [{"alert": str(e)}, 500]

    async def edit_contact(self, _id_user: str, contact_name: str, contact: Contacts) -> list:
        try:
            user: list = await self.get_contact(_id_user, contact_name)

            if user[1] == 200:
                await self.__db_users.users.update_one(
                    {"_id": ObjectId(_id_user), "contacts.name": contact_name},
                    {"$set": {"contacts.$": jsonable_encoder(contact)}}
                )
                return [{"message": "Updated contact"}, 202]
            else:
                return user

        except Exception as e:
            return [{"alert": str(e)}, 500]

    async def del_contact(self, _id_user: str, contact_name: str) -> list:
        try:
            user: list = await self.get_contact(_id_user, contact_name)

            if user[1] == 200:

                self.__db_users.users.update_one(
                    {"_id": ObjectId(_id_user)},
                    {"$pull": {"contacts": {"name": contact_name}}}
                )
                return [{"message": "Deleted contact"}, 200]
            else:
                return user

        except Exception as e:
            return [{"alert": str(e)}, 500]

    async def add_contact_to_group(self, _id_context, contact_name: str, group_name: str) -> list:
        try:
            group: list = await self.get_group(_id_context, group_name)
            contact: list = await self.get_contact(_id_context, contact_name)

            if group[1] == 200:

                if contact[1] == 200:
                    contact[0]["relationship"] = group_name

                    await self.__db_users.users.update_one(
                        {"_id": ObjectId(_id_context), "groups.group_name": group_name},
                        {"$push": {"groups.$.contacts": jsonable_encoder(contact[0])}}
                    )
                    return [{"message": f"Contact added in {group_name}"}, 200]
                else:
                    return contact
            else:
                return group

        except Exception as e:
            return [{"alert": str(e)}, 500]

    async def get_groups(self, _id_context: str) -> list:
        try:
            user: list = await self.get_user(_id_context)

            if user[1] == 200:
                return [user[0]["groups"], 200]
            else:
                return user

        except Exception as e:
            return [{"alert": str(e)}, 500]

    async def get_group(self, _id_user: str, group_name: str) -> list:
        try:
            user: list = await self.get_user(_id_user)

            if user[1] == 200:
                group: dict = await self.__db_users.users.find_one(
                    {"_id": ObjectId(_id_user)},
                    {"groups": {"$elemMatch": {"group_name": group_name}}}
                )

                if len(group) > 1:
                    return [group["groups"][0], 200]
                else:
                    return [{"alert": "Not found group"}, 404]

            else:
                return user

        except Exception as e:
            return [{"alert": str(e)}, 500]

    async def set_group(self, _id_user, group: Group) -> list:
        try:
            user: list = await self.get_user(_id_user)

            if user[1] == 200:
                await self.__db_users.users.update_one(
                    {"_id": ObjectId(_id_user)},
                    {"$push": {"groups": jsonable_encoder(group)}}
                )
                return [{"message": "Added group"}, 201]
            else:
                return user

        except Exception as e:
            return [{"alert": str(e)}, 500]

    async def del_group(self, _id_user: str, group_name: str) -> list:
        try:
            group: list = await self.get_group(_id_user, group_name)

            if group[1] == 200:
                await self.__db_users.users.update_one(
                    {"_id": ObjectId(_id_user)},
                    {"$pull": {"group": {"group_name": group_name}}}
                )
                return [{"message": "Deleted group"}, 200]
            else:
                return group

        except Exception as e:
            return [{"alert": str(e)}, 500]
