import pytest
import json
from main import process_log_file, report_average

# данные
TEST_LOG = """
{"url": "/api/homeworks/", "response_time": 0.1}
{"url": "/api/context/", "response_time": 0.2}
"""


@pytest.fixture
def temp_log_file(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text(TEST_LOG)
    return str(log_file)


def test_process_log_file(temp_log_file):
    result = process_log_file(temp_log_file)
    assert result['/api/homeworks/']['total'] == 1
    assert result['/api/context/']['total'] == 1
    assert result['/api/homeworks/']['sum_time'] == 0.1
    assert result['/api/context/']['sum_time'] == 0.2


def test_report_average(temp_log_file):
    result = report_average([temp_log_file])
    assert '/api/homeworks/' in result
    assert result['/api/homeworks/']['avg_response_time'] == 0.1
    assert result['/api/context/']['avg_response_time'] == 0.2
