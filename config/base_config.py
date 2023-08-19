'''
Description: desc
Author: Firmin.Sun
Date: 2023-08-10 09:36:01
FilePath: \MediaCrawler\config\base_config.py
'''
# Desc: base config
PLATFORM = "xhs"
keywords = ""
userids = ""

LOGIN_TYPE = "qrcode"  # qrcode or phone or cookie
COOKIES = ""  # login by cookie, if login_type is cookie, you must set this value

# enable ip proxy
ENABLE_IP_PROXY = False

# retry_interval
RETRY_INTERVAL = 60 * 30  # 30 minutes

# playwright headless
HEADLESS = True

# save login state
SAVE_LOGIN_STATE = True

# save user data dir
USER_DATA_DIR = "%s_user_data_dir"  # %s will be replaced by platform name

# crawler max notes count
CRAWLER_MAX_NOTES_COUNT = 20000

# max concurrency num
MAX_CONCURRENCY_NUM = 10
