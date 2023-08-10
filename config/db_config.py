import os

# redis config
REDIS_DB_HOST = "127.0.0.1"  # your redis host
REDIS_DB_PWD = os.getenv("REDIS_DB_PWD", "123456")  # your redis password

# mysql config
# RELATION_DB_PWD = os.getenv("RELATION_DB_PWD", "Zhongju885533")  # your relation db password
# RELATION_DB_URL = f"mysql://predemo:{RELATION_DB_PWD}@rm-wz9f660c9bt2nfab8co.mysql.rds.aliyuncs.com:3306/predictdemo"

RELATION_DB_PWD = os.getenv("RELATION_DB_PWD", "123456")  # your relation db password
RELATION_DB_URL = f"mysql://root:{RELATION_DB_PWD}@192.168.1.136:3306/media_crawler"


# save data to database option
IS_SAVED_DATABASED = True  # if you want to save data to database, set True
