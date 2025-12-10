import requests
import json
import allure
from common.recordlog import mylog
from conf.setting import API_TIMEOUT
class SendRequests:
    
    # 发送请求
    def send_requests(self,**kwargs):
        cookie = {}
        session = requests.session()
        result = session.request(**kwargs)
        set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
        if set_cookie:
            cookie['CooKie'] = set_cookie
            # todo 把cookie写入到extract.yaml文件中去
        mylog.info('接口返回信息: %s' % result.text if result.text else result)
        return result

    # 发送请求主方法 最终在standyaml中会调用到该方法
    def run_main(self,name,case_name,url,header,method,cookies = None,file= None,**kwargs):
        try:
            mylog.info(f'接口名称为：{name}')
            mylog.info(f'接口请求地址为：{url}')
            mylog.info(f'测试用例名称为：{case_name}')
            mylog.info(f'接口请求方式：{method}')
            mylog.info(f'请求头为：{header}')
            mylog.info(f'cookies 为：{cookies}')
            req_params = json.dumps(kwargs, ensure_ascii=False)
            # todo 请求参数添加到allure附件中去
            if 'data' in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                mylog.info(f'请求参数为{kwargs}')
            elif 'json' in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                mylog.info(f'请求参数为{kwargs}')
            elif 'params' in kwargs.keys():
                allure.attach(req_params, '请求参数', allure.attachment_type.TEXT)
                mylog.info(f'请求参数为{kwargs}')

            response = self.send_requests(method=method, url=url, headers=header, cookies=cookies, files=file,
                                          timeout=API_TIMEOUT, verify=False, **kwargs)
            return response
        except Exception as e:
            mylog.error(e)
if __name__ == '__main__':
    testFlag = 2
    if testFlag == 1:
        url = 'http://127.0.0.1:8787/dar/user/login'
        payload = {'user_name': 'test01', 'passwd': 'admin123'}
        send = SendRequests()
        res = send.send_requests(method='post', url=url, data=payload)
        print(res.json())

    if testFlag == 2:
        url = 'http://127.0.0.1:8787/dar/user/login'
        payload = {'user_name': 'test01', 'passwd': 'admin123'}
        send = SendRequests()
        header = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
        res = send.run_main(name='测试登录接口',case_name='登录接口请求成功',url=url,header=header,method='post',data = payload)
        print(res)