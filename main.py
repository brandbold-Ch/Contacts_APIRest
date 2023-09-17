from typing import List, Dict
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from Models.models import Contacts, Group, User
from Services.logistic import ApiService
import json

app = FastAPI()
service = ApiService()


@app.post("/create/user")
async def add_user(user_data: User) -> JSONResponse:
    new_user: list = await service.create_user(user_data)
    return JSONResponse(content=new_user[0], status_code=new_user[1])


@app.put("/user/{_id}/update")
async def update_user(_id: str, user_data: User) -> JSONResponse:
    modified_user: list = await service.edit_user_context(_id, user_data)
    return JSONResponse(content=modified_user[0], status_code=modified_user[1])


@app.get("/users")
async def users() -> JSONResponse:
    all_users: list = await service.get_users()
    return JSONResponse(content=all_users[0], status_code=all_users[1])


@app.get("/user/{_id}")
async def user(_id: str) -> JSONResponse:
    new_user: list = await service.get_user(_id)
    return JSONResponse(content=new_user[0], status_code=new_user[1])


@app.get("/user/{id_context}/contacts", response_model=List[Contacts])
async def contacts(id_context: str) -> JSONResponse:
    all_contacts: list = await service.get_contacts(id_context)
    return JSONResponse(content=all_contacts[0], status_code=all_contacts[1])


@app.get("/user/{id_context}/contact/{contact_name}", response_model=Dict[str, str])
async def contact(id_context: str, contact_name: str) -> JSONResponse:
    a_contact: list = await service.get_contact(id_context, contact_name)
    return JSONResponse(content=a_contact[0], status_code=a_contact[1])


@app.post("/user/{id_context}/contact/new")
async def add_contact(id_context: str, contact_data: Contacts) -> JSONResponse:
    new_contact: list = await service.set_contact(id_context, contact_data)
    return JSONResponse(content=new_contact[0], status_code=new_contact[1])


@app.put("/user/{id_context}/contact/{contact_name}/update")
async def update_contact(id_context: str, contact_name: str, contact_data: Contacts) -> JSONResponse:
    modified_contact: list = await service.edit_contact(id_context, contact_name, contact_data)
    return JSONResponse(content=modified_contact[0], status_code=modified_contact[1])


@app.delete("/user/{id_context}/contact/{contact_name}/delete")
async def delete_contact(id_context: str, contact_name: str) -> JSONResponse:
    del_contact: list = await service.del_contact(id_context, contact_name)
    return JSONResponse(content=del_contact[0], status_code=del_contact[1])


@app.get("/user/{id_context}/groups")
async def groups(id_context: str) -> JSONResponse:
    all_groups: list = await service.get_groups(id_context)
    print(json.dumps(all_groups[0], indent=4))
    return JSONResponse(content=all_groups[0], status_code=all_groups[1])


@app.get("/user/{id_context}/group/{group_name}")
async def group(id_context: str, group_name: str) -> JSONResponse:
    a_group: list = await service.get_group(id_context, group_name)
    return JSONResponse(content=a_group[0], status_code=a_group[1])


@app.post("/user/{id_context}/group/new")
async def add_group(id_context: str, group_data: Group) -> JSONResponse:
    new_group: list = await service.set_group(id_context, group_data)
    return JSONResponse(content=new_group[0], status_code=new_group[1])


@app.delete("/user/{id_context}/group/{group_name}/delete")
async def delete_group(id_context: str, group_name) -> JSONResponse:
    del_group: list = await service.del_group(id_context, group_name)
    return JSONResponse(content=del_group[0], status_code=del_group[1])


@app.post("/user/{id_context}/contact/{contact_name}/add/group/{group_name}")
async def add_to_group(id_context: str, contact_name: str, group_name: str) -> JSONResponse:
    add: list = await service.add_contact_to_group(id_context, contact_name, group_name)
    return JSONResponse(content=add[0], status_code=add[1])
