import os
# 项目工程路径
DIR_PATH  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

API_TIMEOUT = 10
# 路径配置
FILE_PATH = {
    'LOG_INI_PATH': os.path.join(DIR_PATH,'conf','loguru.ini'),
    'LOG_PATH': os.path.join(DIR_PATH,'output','log'),
    'LOGIN_YAML': os.path.join(DIR_PATH,'testcase','LoginAPi','login.yaml'),
    'EXTRACT':os.path.join(DIR_PATH,'extract.yaml'),
    'CONFIG': os.path.join(DIR_PATH,'conf','config.ini')
}

