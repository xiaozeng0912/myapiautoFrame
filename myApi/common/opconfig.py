import configparser

from conf.setting import FILE_PATH

class OperationConfig:
    # 初始化获取读取配置文件对象
    def __init__(self,file_path = None):
        # 默认读取config.ini
        if file_path is not None:
            self.file_path = file_path
        else:
            self.file_path = FILE_PATH['CONFIG']
        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.file_path, encoding='utf-8')
        except Exception as e:
            print(e)

    def get_section_for_data(self, section, option):
        try:
            values = self.conf.get(section, option)
            return values
        except Exception as e:
            print(e)

    def get_api_host(self):
        return self.get_section_for_data('api_host','host_url')

if __name__ == '__main__':
    print(OperationConfig().get_api_host())
