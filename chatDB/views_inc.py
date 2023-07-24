import asyncio
import json
import traceback

import paramiko

from utils.file_utils import write_file, read_file, write_file_table_data
from utils.mysql_utils import MysqlPool, db_con, create_conn
from utils.request_utils import make_request, make_request_stream
from common.log import logger


async def chatGpt_logic(text):
    url = "https://www.chatgptplus.one/v1/chat/completions"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0',
        'Content-Type': 'application/json',
        "authorization": "Bearer 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",
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": "假设你是个SQL编辑器，接下来你返回的SQL代码要和其他内容分隔，非SQL代码内容的每一行前面追加-- \n请根据以下table properties和SQL input将自然语言转换成SQL查询. \nMYSQL SQL tables, with their properties:\nauth_group(id, name)\nauth_user_user_permissions(id, user_id, permission_id)\nclickhouse_mysql_table(int_id, float)\nauth_user(id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, pwd_lock, pwd_last_modify)\nauth_permission(id, name, content_type_id, codename)\nauth_user_groups(id, user_id, group_id)\naccount_userprofile(id, Fdepartment, user_id)\nauth_group_permissions(id, group_id, permission_id)，不需要做过多的解释，只需要按照我所定义的回复"
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "model": "gpt-3.5-turbo",
        "stream": True,
        "temperature": 1,
        "top_p": 1
    }
    payload = json.dumps(data)
    result = ""
    async for chunk in make_request_stream("POST", url, headers=headers, data=payload):
        if chunk:
            try:
                chunk = chunk.decode()
                chunk = chunk.replace("data: ", "").replace("\n", "")
                if "]}{" in chunk:
                    chunk = "{" + chunk.split("]}{")[1]
                chunk = json.loads(chunk)
                content = chunk["choices"][0]["delta"].get("content")
                if content is not None:
                    result = result + content
                    # print(content, end="")
            except:
                await logger.debug(traceback.format_exc())
    return result


async def execute_sql_logic(sql):
    """ 执行sql语句 """
    mysql_pool = MysqlPool()
    results = await mysql_pool.select_mysql_all(sql)
    return results


async def query_table_data_logic(table_name, offset=0, limit=100):
    """ 获取数据表数据 """
    sql = "select * from %s limit %d,%d" % (table_name, offset, limit)
    mysql_pool = MysqlPool()
    results = await mysql_pool.select_mysql_all(sql)
    return results


async def export_table_data_logic(table_name, count=100000):
    """ 导数据 """
    sql = "select * from %s limit %d" % (table_name, count)
    mysql_pool = MysqlPool()
    results = await mysql_pool.select_mysql_all(sql)
    await write_file_table_data(table_name, results)
    return results


# async def import_table_data(table_name, file):


async def get_table_index_logic(table_name):
    """ 获取表索引 """
    sql = "SHOW INDEX FROM %s" % table_name
    mysql_pool = MysqlPool()
    results = await mysql_pool.select_mysql_all(sql)
    return results


async def get_database_logic():
    """ 获取所有数据库 """
    sql = "SHOW DATABASES;"
    mysql_pool = MysqlPool()
    results = await mysql_pool.select_mysql_all(sql)
    return results


async def get_tables_by_database_logic():
    """ 获取当前数据库下的所有表 """
    sql = "SHOW TABLES;"
    mysql_pool = MysqlPool()
    results = await mysql_pool.select_mysql_all(sql)
    data_list = []
    for item in results:
        for k, v in item.items():
            data_list.append(v)
    return data_list


async def get_table_desc_logic(table_name):
    """ 获取数据库表ddl """
    mysql_pool = MysqlPool()
    sql = "SHOW CREATE TABLE {};".format(table_name)
    results = await mysql_pool.select_mysql_all(sql)
    return results


async def connection_db_logic(conn_conf: dict):
    """
    连接数据库
    conn_conf = {
        "db": {
            "name": "test",
            "host": "127.0.0.1",
            "prot": "3643",
            "database": "空/aaa",
        },
        "ssh": {
            "host": "127.0.0.1",
            "port": "36000",
            "username": "",
            "password": ""
        }
    }
    :param conn_info:
    :return:
    """
    ssh_info = conn_conf["ssh"]
    db_info = conn_conf["db"]
    await create_conn(db_info, ssh_info)
    await add_database_conf_logic(conn_conf)


async def test_connection_db_logic(conn_conf: dict):
    """
    测试连接数据库
    :param conn_conf:
    :return:
    """
    ssh_info = conn_conf["ssh"]
    db_info = conn_conf["db"]
    await create_conn(db_info, ssh_info)
    mysql_pool = MysqlPool()
    await mysql_pool.close()
    return "测试连接成功"


async def test_ssh_logic(ssh_conf: dict):
    """
    测试ssh连接
    ssh_conf = {
        "ssh": {
                "host": "127.0.0.1",
                "port": "36000",
                "username": "",
                "password": ""
            }
    }
    :param ssh_conf:
    :return:
    """
    # 创建SSH客户端
    client = paramiko.SSHClient()
    # 设置自动添加主机密钥
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 连接SSH服务器
    try:
        client.connect(ssh_conf["host"], port=ssh_conf["port"], username=ssh_conf["username"],
                       password=ssh_conf['password'])
        return "测试连接成功"
    except paramiko.AuthenticationException as auth_exception:
        raise ('认证失败', str(auth_exception))
    except paramiko.SSHException as ssh_exception:
        raise ('SSH连接失败:', str(ssh_exception))
    finally:
        # 关闭连接
        client.close()


async def add_database_conf_logic(conn_info):
    """ 添加连接配置 """
    str_res = await read_file()
    db_name = conn_info["db"]["name"]
    if db_name.encode('unicode_escape').decode() not in str_res:
        json_res = json.loads(str_res)
        json_res["conn_all"].append(conn_info)
        json_res["conn_all"] = json_res["conn_all"]
        await write_file(json.dumps(json_res))


async def get_database_conf_logic():
    """ 获取已保存的配置 """
    str_res = await read_file()
    return json.loads(str_res)


async def main():
    # res = await chatGpt("获取某个表的结构")
    # res = await get_tables_by_database("tme_monitor_test")
    # res = await get_table_desc("tme_monitor", "t_monitor_data_wangyi_baike_tags")
    ssh_info = {
        "host": "9.134.84.76",
        "port": "36000",
        "username": "user_01",
        "password": "Music@2017"
    }
    res = await test_ssh_logic(ssh_info)
    # print(res)


if __name__ == '__main__':
    asyncio.run(main())
