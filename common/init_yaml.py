import yaml

from common.file_path import file_path
from utils.common_utils import get_local_ip

yaml_file = "chatDB.yaml"
local_ip = get_local_ip()
if "192.168" in local_ip:
    yaml_file = "chatDB_test.yaml"
# 读取YAML文件
with open("{}/conf/{}".format(file_path, yaml_file), "r") as stream:
    try:
        yaml_data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        ymal_data = {}
        print(exc)
