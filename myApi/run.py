import os
import shutil
import pytest

if __name__ == '__main__':
    pytest.main(['-s', '-v', '--alluredir=./output/report/temp', './testcase', '--clean-alluredir'])
    shutil.copy('./environment.xml', './output/report/temp')
    #os.system(f'allure serve ./output/report/temp')
