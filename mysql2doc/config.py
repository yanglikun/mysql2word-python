__author__ = 'yanglikun'
from collections import namedtuple
import os

DBConfig = namedtuple("dbConfig", ["userName", "password", "host","port","databaseName", "charset"])

# 加载文件
configMap = {}
with open(os.path.dirname(os.path.abspath(__file__)) + '/../config.properties') as configFile:
    for line in configFile.read().splitlines():
        lineSplit = line.split("=")
        configMap[lineSplit[0]] = lineSplit[1]

# 数据库配置
dbConfig = DBConfig(configMap['db.userName'],
                    configMap['db.password'],
                    configMap['db.host'],
                    configMap['db.port'],
                    configMap['db.databaseName'],
                    configMap['db.charset'])


def checkdbconfig(dbConfig):
    if not (dbConfig.userName and dbConfig.password and dbConfig.host and dbConfig.databaseName and dbConfig.charset):
        raise Exception("先在config.properties配置数据库连接信息")


checkdbconfig(dbConfig)
dbConfigMap = {}
for key, value in dbConfig._asdict().items():
    dbConfigMap[key] = value
