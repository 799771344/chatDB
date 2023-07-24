import pymysql

from pymysql import cursors
from dbutils.pooled_db import PooledDB
from sshtunnel import SSHTunnelForwarder


async def create_conn(db_info, ssh_info, cursorclass="dict"):
    if cursorclass == "dict":
        cursorclass = cursors.DictCursor
    elif cursorclass == "tuple":
        cursorclass = cursors.Cursor
    global db_con
    if ssh_info:
        # 本地ssh链接
        services = SSHTunnelForwarder(
            (ssh_info["host"], ssh_info["port"]),  # B机器的配置--跳板机
            ssh_password=ssh_info["password"],  # B机器的配置--跳板机账号
            ssh_username=ssh_info["username"],  # B机器的配置--跳板机账户密码
            remote_bind_address=(db_info["host"], db_info["port"]))  # A机器的配置-MySQL服务器

        services.start()
        pool = PooledDB(
            creator=pymysql,  # 数据库类型
            maxconnections=10,  # 连接池最大连接数量
            mincached=0,  # 初始化时连接池中最少连接数量
            maxcached=10,  # 连接池最大缓存数量，超过这个数量的连接会被关闭
            maxshared=10,  # 连接池中最多被共享的连接数量，0表示所有连接都不共享
            blocking=True,  # 连接请求过多时是否阻塞等待连接，默认为True
            maxusage=None,  # 单个连接最大使用次数，None表示不限制
            setsession=None,  # 在连接上执行一条语句来设置会话，如“SET TIMEZONE='UTC'”
            ping=30,  # 使用ping测试连接是否有效的时间间隔，0表示不测试
            host='127.0.0.1',
            port=services.local_bind_port,
            user=db_info["user"],  # A机器的配置-MySQL服务器账户
            password=db_info["password"],  # A机器的配置-MySQL服务器密码c
            db=db_info["database"],  # 可以限定，只访问特定的数据库,否则需要在mysql的查询或者操作语句中，指定好表名
            charset="utf8mb4",
            cursorclass=cursorclass,
        )
    else:
        pool = PooledDB(
            creator=pymysql,  # 数据库类型
            maxconnections=10,  # 连接池最大连接数量
            mincached=0,  # 初始化时连接池中最少连接数量
            maxcached=10,  # 连接池最大缓存数量，超过这个数量的连接会被关闭
            maxshared=10,  # 连接池中最多被共享的连接数量，0表示所有连接都不共享
            blocking=True,  # 连接请求过多时是否阻塞等待连接，默认为True
            maxusage=None,  # 单个连接最大使用次数，None表示不限制
            setsession=None,  # 在连接上执行一条语句来设置会话，如“SET TIMEZONE='UTC'”
            ping=30,  # 使用ping测试连接是否有效的时间间隔，0表示不测试
            host=db_info["host"],
            port=db_info["port"],
            user=db_info["user"],
            password=db_info["password"],
            db=db_info["database"],
            charset="utf8mb4",
            cursorclass=cursorclass,
        )
    db_con = pool


db_con = None


class MysqlPool(object):
    async def save_mysql(self, sql, args=[]):
        """
        保存数据库
        :param sql: 执行sql语句
        :param args: 添加的sql语句的参数 list[tuple]
        """
        db = await self.get_connection()
        cursor = db.cursor()
        if len(args) > 0:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        db.commit()
        cursor.close()

    async def select_mysql(self, sql, args=[]):
        db = await self.get_connection()
        cursor = db.cursor()
        if len(args) > 0:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    async def select_mysql_all(self, sql, args=[]):
        db = await self.get_connection()
        cursor = db.cursor()
        if len(args) > 0:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    async def switch_db(self, db_name):
        """更换数据库"""
        global db_con
        db_con.db = db_name

    async def close(self):
        db_con.close()

    async def get_connection(self):
        db = db_con.connection()
        return db
