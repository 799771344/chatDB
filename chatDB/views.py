from chatDB.views_inc import *
from pydantic import BaseModel


async def response_json(code, message, data={}):
    return {"code": code, "message": message, "data": data}


class DBConf(BaseModel):
    name: str
    host: str
    prot: int
    user: str
    password: str
    database: str


class SSHConf(BaseModel):
    name: str
    host: str
    prot: int
    username: str
    password: str


class ConnConf(BaseModel):
    db: DBConf
    ssh: SSHConf


async def connection_db(conn_conf: dict):
    await connection_db_logic(conn_conf)
    return await response_json(0, "success")


async def get_tables_by_database():
    res = await get_tables_by_database_logic()
    return await response_json(0, "success", res)


async def get_database_conf():
    res = await get_database_conf_logic()
    return await response_json(0, "success", res)


async def execute_sql(sql: str):
    res = await execute_sql_logic(sql)
    return await response_json(0, "success", res)


async def chatGpt(test: str):
    res = await chatGpt_logic(test)
    return await response_json(0, "success", res)
