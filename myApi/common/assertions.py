import allure
import jsonpath
import operator
from common.recordlog import mylog

# 断言处理
class Assertions:
    # 包含断言 这里的expected 是value值 例 {'msg':'登录成功'}
    def assert_contains(self,value,response,status_code):
        flag = 0
        for assert_key,assert_value in value.items():
            # 断言 status
            if assert_key == 'status_code':
                # 断言 响应状态码
                if assert_value != status_code:
                    flag = flag + 1
                    mylog.error(f'contains断言失败：接口返回码 {status_code} 不等于 {assert_value}')
            else:
                #
                resp_list = jsonpath.jsonpath(response, "$..%s" % assert_key)
                if isinstance(resp_list[0], str):
                    resp_list = ''.join(resp_list)
                if resp_list:
                    # 判断 预期结果中的value值的情况 ： 整型
                    if isinstance(assert_value, int):
                        assert_value = assert_value
                    elif isinstance(assert_value, str):
                        assert_value = None if assert_value.upper() == 'NONE' else assert_value
                    if assert_value in resp_list:
                        mylog.info(f"字符串包含断言成功：预期结果-->{assert_value}；实际结果-->{resp_list}")

                        # 在allure报告中体现
                        allure.attach(f"预期结果：{assert_value}\n实际结果：{resp_list}", '响应文本断言结果：成功',
                                      attachment_type=allure.attachment_type.TEXT)
                    else:
                        flag = flag + 1
                        allure.attach(f"预期结果：{assert_value}\n实际结果：{resp_list}", '响应文本断言结果：失败',
                                      attachment_type=allure.attachment_type.TEXT)

                        mylog.error(f"响应文本断言失败：预期结果为{assert_value},实际结果为 {resp_list}")
        return flag

    # 等值断言 equal assert validation
    def equal_assert(self, expected_results, actual_results):
        '''
        :param expected_results: 预期结果
        :param actual_results: 实际结果
        :return:
        '''
        """相等断言"""
        flag = 0
        res_lst = []
        if isinstance(actual_results, dict) and isinstance(expected_results, dict):
            for res in actual_results:
                if list(expected_results.keys())[0] != res:
                    res_lst.append(res)
            for rl in res_lst:
                del actual_results[rl]
            eq_assert = operator.eq(actual_results, expected_results)
            if eq_assert:
                mylog.info(f"相等断言成功：接口实际结果：{actual_results}，等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{actual_results}", '相等断言结果：成功',
                              attachment_type=allure.attachment_type.TEXT)
            else:
                flag += 1
                mylog.error(f"相等断言失败：接口实际结果{actual_results}，不等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{actual_results}", '相等断言结果：失败',
                              attachment_type=allure.attachment_type.TEXT)
        else:
            raise TypeError('相等断言--类型错误，预期结果和接口实际响应结果必须为字典类型！')
        return flag

    def assert_result(self,expected,response,status_code):
        '''
        :param expected: yaml文件中 validation的值
        :param response: 响应结果
        :param status_code: 响应状态码
        :return:
        '''
        all_flag = 0
        try:
            for yq in expected:
                for key,value in yq.items():
                    if key == 'contains':
                        # 调用断言包含的方法
                        flag = self.assert_contains(value,response,status_code)
                        all_flag = flag + all_flag

                    elif key == 'equal':
                        # 调用断言相等方法
                        flag = self.equal_assert(value,response)
                        all_flag = flag + all_flag
                    elif key == 'db':
                        pass
                    else:
                        mylog.error(f'暂不支持{key}这种断言模式！')
        except Exception as e:
            mylog.error('请检查断言字段是否包含在接口的返回值中')
            mylog.error(f'异常信息：{e}')
            raise e
        if all_flag == 0:
            mylog.info('测试成功')
            assert True
        else:
            mylog.error('测试失败')
            assert False


