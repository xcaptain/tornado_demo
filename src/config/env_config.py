import os

# http api 相关配置
APP_PORT = int(os.environ.get("APP_PORT"))

# mysql 相关配置
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT"))
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWD = os.environ.get("MYSQL_PASSWD")
IS_DEBUG = True if os.environ.get("IS_DEBUG") else False

# redis 相关配置
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = int(os.environ.get("REDIS_PORT"))
REDIS_DB = int(os.environ.get("REDIS_DB"))
