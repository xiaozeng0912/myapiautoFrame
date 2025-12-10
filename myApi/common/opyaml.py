import os.path
import pprint
import yaml
from conf.setting import FILE_PATH

# 获取测试用例
def get_test_case_yaml(file_path):
    testlist = []
    with open(file=file_path, mode='r', encoding='utf-8') as fr:
        data = yaml.safe_load(fr)
    # yaml格式是 [{'baseInfo':'value'},'testcase':[case1],[case2]]
    # 最外层就是一个列表 所以是 len(data) <= 1
    if len(data) <= 1:
        yaml_data = data[0]
        baseInfo = yaml_data.get('baseInfo')
        testCases = yaml_data.get('testCase')
        for ts in testCases:
            param = [baseInfo, ts]
            testlist.append(param)
        return testlist
    else:
        return data

# 操作yaml文件
class OperationYaml:

    # 获取extract.yaml中的数据
    def get_extract_yaml(self,node_name,second_name =None):
        # 首先判断yaml文件是否存在
        if os.path.exists(FILE_PATH['EXTRACT']):
            pass
        else:
            print('extract 不存在 下面自己创建')
            fs = open(FILE_PATH['EXTRACT'],'w')
            fs.close()
            print('extract 创建成功')
        try:
            with open(file=FILE_PATH['EXTRACT'],mode='r',encoding='utf-8')as fr:
                data = yaml.safe_load(fr)
            if second_name:
                extract_data = data[node_name][second_name]
                return extract_data
            else:
                extract_data = data[node_name]
                return extract_data
        except Exception as e:
            print('读取extract文件错误')
            raise e
    # 写入数据到extract.yaml中去
    def write_yaml(self,data):
        file_path = FILE_PATH['EXTRACT']
        if not os.path.exists(file_path):
            os.system(file_path)
        try:
            with open(file=file_path,mode='w',encoding='utf-8')as fw:
                if isinstance(data,dict):
                    write_data =yaml.dump(data,allow_unicode=True,sort_keys=False)
                    fw.write(write_data)
                else:
                    print('写入extract.yaml文件的数据必须是字典格式')
        except Exception as e:
            print(e)


    # 清除extract.yaml
    def clear_extract_yaml(self):
        """
        清除extract.yaml文件的数据
        :return:
        """
        with open(FILE_PATH['EXTRACT'], 'w') as f:
            f.truncate()

if __name__ == '__main__':
    testFlag = 1
    if testFlag == 1:
        file_path = FILE_PATH['LOGIN_YAML']
        result = get_test_case_yaml(file_path)
        pprint.pprint(*result)
        # print(result)
        # print(result[0]['baseInfo'])
    if testFlag == 2:
        result = OperationYaml().get_extract_yaml('token')
        print(result)

    if testFlag == 3:
        data= {'cookie':'token_header_dasd'}
        OperationYaml().write_yaml(data)

