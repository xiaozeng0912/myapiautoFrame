from common.opyaml import OperationYaml
import re,random
# 热加载方法
class HotLoads:
    def __init__(self):
        self.read = OperationYaml()

    def get_extract_order_data(self,data,randoms):
        """获取extract.yaml数据，不为0、-1、-2，则按顺序读取文件key的数据"""
        if randoms not in [0, -1, -2]:
            return data[randoms - 1]


    # 获取extract.yaml文件中的数据
    def get_extract_data(self,node_name,randoms = None):
        data = self.read.get_extract_yaml(node_name)
        if randoms is not None and bool(re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$').match(randoms)):
            randoms = int(randoms)
            data_value = {
                randoms: self.get_extract_order_data(data, randoms),
                0: random.choice(data),
                -1: ','.join(data),
                -2: ','.join(data).split(','),
            }
            data = data_value[randoms]
        else:
            data = self.read.get_extract_yaml(node_name, randoms)
        return data


if __name__ == '__main__':

    testFlag = 1
    if testFlag == 1:
        result = HotLoads().get_extract_data('header', 'content-type')
        print(result)
    if testFlag == 2:
        res = HotLoads().get_extract_data()
        print(res)