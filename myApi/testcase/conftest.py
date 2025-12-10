import time
import pytest
from common.recordlog import mylog


@pytest.fixture(autouse=True)
def start_and_end():
    mylog.info('-----------------接口测试开始---------------------')
    yield
    mylog.info('-----------------接口测试结束---------------------')

def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和 nodeid 的中文显示
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

# 测试用例结果收集
def pytest_terminal_summary(terminalreporter,exitstatus,config):

    print(terminalreporter.stats)
    # 收集测试用例总数
    case_total = terminalreporter._numcollected
    # 收集测试用例通过数
    passed = len(terminalreporter.stats.get('passed', []))
    # 收集测试用例失败数
    failed = len(terminalreporter.stats.get('failed', []))
    # 收集测试用例错误数量
    error = len(terminalreporter.stats.get('error', []))
    # 收集测试用例跳过执行数
    skipped = len(terminalreporter.stats.get('skipped', []))
    # 收集测试用例执行时长
    duration = time.time() - terminalreporter._sessionstarttime

    # 将报告结果写到log日志中去
    mylog.success(f"""
              各位好，本次XXX智慧物流项目的接口自动化测试结果如下，请注意失败及错误的接口：
              测试用例总数：{case_total}个
              通过数：{passed}个
              失败数：{failed}个
              跳过执行数：{skipped}个
              错误异常：{error}个
              测试用例执行时长：{duration}
              点击查看测试报告：http://192.168.112.59:8088/job/ZHWLXM/138/allure/
              """)

    # todo
    # 需要部署到Jenkins持续集成当中去运行
    # oper = OperJenkins()
    # report = oper.report_success_or_fail()


    content = f"""
           各位好，本次XXX智慧物流项目的接口自动化测试结果如下，请注意失败及错误的接口：
           测试用例总数：{case_total}个
           通过数：{passed}个
           失败数：{failed}个
           跳过执行数：{skipped}个
           错误异常：{error}个
           测试用例执行时长：{duration}
           点击查看测试报告：http://192.168.112.59:8088/job/ZHWLXM/138/allure/
           """
    # send_dingding_msg(content=content)