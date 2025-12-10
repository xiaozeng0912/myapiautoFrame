import allure
import pytest
from base.apiutls import RequestBase
from base.generateId import c_id,m_id
from conf.setting import FILE_PATH
from common.opyaml import get_test_case_yaml
@allure.feature('测试项目')
class TestLogin:
    @allure.story(next(c_id)+'登录接口')
    @pytest.mark.parametrize('base_info,test_case',get_test_case_yaml(FILE_PATH['LOGIN_YAML']))
    def test_login(self,base_info,test_case):
        # 获取用例标题
        allure.dynamic.title(test_case['case_name'])
        RequestBase().specification_yaml(base_info,test_case)

if __name__ == '__main__':
    pytest.main(['-sv'])