import os
from configparser import ConfigParser
from time import strftime
from loguru import logger
from conf import setting

# 配置文件路径
LOG_INI_PATH  = setting.FILE_PATH['LOG_INI_PATH']
# 日志输出路径
LOG_PATH = setting.FILE_PATH['LOG_PATH']
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

class Mylog:
    _instance = None
    _call_flag = True
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_log(self):
        if self._call_flag:
            __curdate = strftime('%Y%m%d %H%M%S')
            logger.remove(handler_id=None)  # 关闭控制台输出
            conf = ConfigParser()
            conf.read(LOG_INI_PATH)

            logger.add(
                #
                f'{LOG_PATH}/log_{__curdate}.log',
                level=conf.get('log', 'level'),
                format=conf.get('log', 'format'),
                retention=conf.get('log', 'retention'),
                rotation=conf.get('log', 'rotation'),
                compression=conf.get('log', 'compression'),
                encoding='utf-8'

            )
            self._call_flag = False
        return logger
mylog = Mylog().get_log()

if __name__ == '__main__':
    mylog.info('test')