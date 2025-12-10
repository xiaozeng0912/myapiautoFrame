import json
import re
from json import JSONDecodeError

import allure
import jsonpath
from common.assertions import Assertions
from common.hotload import HotLoads
from common.opconfig import OperationConfig
from common.opyaml import OperationYaml, get_test_case_yaml
from common.recordlog import mylog
from common.sendrequest import SendRequests
from conf.setting import FILE_PATH


class RequestBase:
    def __init__(self):
        self.read = OperationYaml()
        self.run = SendRequests()
        self.conf = OperationConfig()
        self.asserts = Assertions()
    # 解析替换数据 ${}   --假如数据是 ${get_token(params)}
    def replace_data(self,data):
        str_data = data
        # 判断data数据格式
        # print(f'解析前的数据{str_data}')
        if isinstance(data,dict) or isinstance(data,list):
            str_data = json.dumps(data,ensure_ascii=False)
        for i in range(str_data.count('${')):
            # 判断 ${} 在转换的字符串中是否存在
            if '${' in str_data and '}' in str_data:
                start_index = str_data.index('$')
                end_index = str_data.index('}',start_index)
                # 找到 对应的值 比如 ${get_token(params)}
                rep_params = str_data[start_index:end_index+1]
                # 获取到对应的方法 和 参数
                func_name = rep_params[2:rep_params.index('(')]
                func_params = rep_params[rep_params.index("(") + 1:rep_params.index(")")]
                extract_data = getattr(HotLoads(),func_name)(*func_params.split(',') if func_params else "")
                # 对于获取的数据是列表的处理
                if extract_data and isinstance(extract_data, list):
                    extract_data = ','.join(e for e in extract_data)
                str_data = str_data.replace(rep_params, str(extract_data))
        # print(f'解析后的数据{str_data}')
        # 还原数据
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    # 规范yaml测试用例 -拿到yaml用例的各个参数进行处理
    def specification_yaml(self,base_info,test_case):
        try:
            api_name = base_info['api_name']
            allure.attach(api_name, f'接口名称：{api_name}', allure.attachment_type.TEXT)
            host_url = self.conf.get_api_host()
            url = host_url + base_info['url']
            allure.attach(api_name, f'接口地址：{url}', allure.attachment_type.TEXT)
            method = base_info['method']
            allure.attach(api_name, f'请求方法：{method}', allure.attachment_type.TEXT)
            header = self.replace_data(base_info['header'])
            allure.attach(api_name, f'请求头：{header}', allure.attachment_type.TEXT)
            # cookies的处理
            cookie = None
            if base_info.get('cookies') is not None:
                cookie = eval(self.replace_data(base_info['cookies']))
            case_name = test_case.pop('case_name')
            allure.attach(api_name, f'测试用例名称：{case_name}', allure.attachment_type.TEXT)
            # 请求参数处理 data json params
            params_type = ['data','json','params']
            for key,value in test_case.items():
                if key in params_type:
                    # 处理动态替换
                    test_case[key] = self.replace_data(value)

            # todo 上传文件处理 files  格式 files =  {变量名:open(文件，rb)}
            file,files = base_info.pop('files',None),None
            if file is not None:
                for fk,fv in file.items():
                    files = {fk,open(fv,'rb')}

            # todo 断言处理 validation
            val = self.replace_data(test_case.get('validation'))
            test_case['validation'] = val
            # eval将字符串转换为字典
            validation = eval(test_case.pop('validation'))

            # todo 返回结果提取值处理 extract / extract_list
            extract = test_case.pop('extract',None)
            extract_list = test_case.pop('extract_list',None)

            # 最终调用下面方法去发送请求
            res = self.run.run_main(name=api_name,case_name=case_name,url=url,header=header,method=method,cookies=cookie,file=files,**test_case)
            status_code = res.status_code
            allure.attach(res.text, f'接口返回信息：{res.text}', allure.attachment_type.TEXT)
            try:
                res_json = json.loads(res.text)
                # 提取单个值
                if extract is not None:
                    self.extract_data(extract,res.text)
                # 提取列表
                if extract_list is not None:
                    self.extract_data(extract_list,res.text)
                self.asserts.assert_result(validation,res_json,status_code)
            except JSONDecodeError as js:
                mylog.error('系统异常或接口未请求！')
                raise js
            except Exception as e:
                mylog.error(e)
                raise e
        except Exception as e:
            mylog.error(e)
            raise e

    # 提取参数
    def extract_data(self,test_case_extract,response):
        '''
        :param test_case_extract:  extract 的值
        :param response:
        :return:
        '''
        # 支持正则表达式和 jsonpath提取器
        pat_lst = ['(.*?)', '(.+?)', r'(\d)', r'(\d*)']
        for key,value in test_case_extract.items():
            for pat in pat_lst:
                if pat in value:
                    ext_lst = re.search(value,response)
                    if pat in [r'(\d+)', r'(\d*)']:
                        extract_data = {key: int(ext_lst.group(1))}
                    else:
                        extract_data = {key: ext_lst.group(1)}
                    # 写入到extract.yaml文件中
                    self.read.write_yaml(extract_data)
            # jsonpath提取
            if '$' in value:
                ext_json = jsonpath.jsonpath(json.loads(response), value)[0]
                if ext_json:
                    extract_data = {key: ext_json}
                    mylog.info(f'提取接口的返回值：{extract_data}')
                else:
                    extract_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                self.read.write_yaml(extract_data)

    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_date = {key: ext_list}
                        mylog.info('正则提取到的参数：%s' % extract_date)
                        self.read.write_yaml(extract_date)
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    mylog.info('json提取到参数：%s' % extract_date)
                    self.read.write_yaml(extract_date)
        except:
            mylog.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')




if __name__ == '__main__':
    send = RequestBase()
    case = get_test_case_yaml(file_path=FILE_PATH['LOGIN_YAML'])[0]
    # print(case[0])
    base_info,test_case = case[0],case[1]
    # print('----ceshi---')
    # print(base_info['api_name'])
    res = send.specification_yaml(base_info,test_case)


