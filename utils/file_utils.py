import asyncio
import csv

import aiofiles
from common.file_path import file_path


async def parse_csv_file_to_data_list(file_path):
    data_list = []
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            data_list.append(line)
    return data_list


async def write_file(db_conf, file_path="{}/etc/db_conf.json".format(file_path)):
    async with aiofiles.open(file_path, mode='w') as file:
        await file.write(db_conf)


async def read_file(file_path="{}/etc/db_conf.json".format(file_path)):
    async with aiofiles.open(file_path, mode='r') as file:
        data = await file.read()
        return data


async def write_file_table_data(table_name, results):
    # 导出查询结果到CSV文件
    filename = f"{table_name}.csv"
    # 提取结果中的所有键，作为CSV文件的列标题
    fieldnames = results[0].keys()
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 写入列标题
        writer.writeheader()
        # 写入每行数据
        writer.writerows(results)
