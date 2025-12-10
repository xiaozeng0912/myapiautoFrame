import pytest
from common.opyaml import OperationYaml

@pytest.fixture(scope='session', autouse=True)
def clear_data():
    OperationYaml().clear_extract_yaml()


