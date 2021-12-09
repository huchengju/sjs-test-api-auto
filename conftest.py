import pytest

from config import url

# def pytest_configure(config):
#
#     config.addinivalue_line("markers", 'api_smoke')

# def pytest_configure(config):
#
#     marker_list = ["api_smoke", "scenes"]
#     for markers in marker_list:
#         config.addinivalue_line("markers", markers)

def pytest_addoption(parser):

    parser.addoption(
        "--envopt", action="store", default="testing", help="my option: testing or prod"
    )

@pytest.fixture(scope='session', autouse=True)
def xyyoption(request):

    envused = request.config.getoption("--envopt")
    if envused == "testing":
        url.testjavaHost = 'http://10.101.12.15:8091'
    elif envused == "prod":
        url.testjavaHost = 'https://javaapi.biliangwang.com'
    else:
        print("Now is not stage environment")
