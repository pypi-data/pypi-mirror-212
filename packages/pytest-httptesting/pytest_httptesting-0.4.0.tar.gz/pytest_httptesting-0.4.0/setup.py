# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['http_testing', 'http_testing.assertion_elements']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=23.1.0,<24.0.0', 'httpx>=0.24.0,<0.25.0', 'pytest>=7.2.0,<8.0.0']

entry_points = \
{'pytest11': ['http_page_checker = http_testing.plugin']}

setup_kwargs = {
    'name': 'pytest-httptesting',
    'version': '0.4.0',
    'description': 'http_testing framework on top of pytest',
    'long_description': '# HTTP_TESTING\n\n## Description\nThis project aims to help to create e2e tests, by chaining http calls and verifications on target pages.\n\n## Concept\nThis project is built on pytest.\n\nEach .py file in test represents several tests scenario on one target site, we can provide the site\'s hostname\nas a local variable, the framework know how to construct http call from that.\n\nEach test function in the .py test file represent a scenario of test which is consisted by several steps. For example,\ntest user\'s account page, first, we authenticate the client by post user\'s name and password,\nthen access the account page to verify some values. Each step is described by calling the variable `check`\nwhich is a pytest fixture.\n\n## Tutorial\n### Install\n```bash\npip install pytest-httptesting\n```\n\n### Create test suite\n```python\n# test/test_example.py\nfrom http_testing.assertions import Assertions, NegativeAssertions\nfrom http_testing.cookie import Cookie\nfrom http_testing.page_checker import PageChecker\nfrom http_testing.validators import Regex\n\nhost = "www.google.com"  # mandatory: used in the `check` fixture\nscheme = "https"  # "https" by default\nport = None  # None by default\n\n\ndef test_scenario_one(check: PageChecker):\n    check(\n        title="Senario One",\n        path="/",\n        should_find=Assertions(\n            status_code=200,\n            content=["<title>Google</title>"],\n            headers={"Content-Type": "text/html; charset=ISO-8859-1"},\n            cookies=[Cookie(name="AEC", value=Regex(r".*"))],\n        ),\n        should_not_find=NegativeAssertions(\n            status_code=400,\n            content=["groot"],\n            headers={"nooooo": ""},\n            cookies=[Cookie(name="nop", value="a")],\n        ),\n        timeout=10,  # you can pass additional kwargs to httpx request\n    )\n\n    assert check.previous_response.status_code == 200  # inspect previous response\n```\n\n### Run test\n```bash\n$ pytest test --tb=no --no-header -v  # traceback is disabled because it is not very useful to anayse the functional error\n============= test session starts =============\ncollected 1 item\n\ntest/test_example.py::test_scenario_one PASSED\n\n============= 1 passed in 0.16s =============\n\n```\n\n### Debug\nIn case of error, a temporary file will be generated, as shown in the `short test summary info`. It is a json file concluding\nresponse content, status code, headers and cookies.\n```bash\n$ pytest test --tb=no --no-header -v\n============= test session starts =============\ncollected 1 item\n\ntest/test_example.py::test_scenario_one FAILED\n\n============= short test summary info =============\nFAILED test/test_example.py::test_scenario_one - AssertionError: Senario One - \'Content-Typessss\':\'text/html; charset=ISO-8859-1\' not found in headers on page \'https://www.google.com/\' - please check file \'/tmp/tmptaowd2u5\'\n============= 1 failed in 1.22s =============\n\n```\n\n### Advanced\n#### Customize the http client configuration\nIt is possible to create a fixture `http_client` to create your own http client.\n```python\n@pytest.fixture\ndef http_client():\n    with Client(verify=False, cookies={"cookie_1": "cookie_value_1"}) as client:\n        yield client\n```\n\n#### Customize the base url\nIt is possible to create a fixture `base_url` to override the default construction of base url.\n```python\nfrom httpx import URL\n@pytest.fixture\ndef base_url() -> URL:\n    return URL("https://www.google.com")\n```\n',
    'author': 'HE Qile',
    'author_email': 'mr.qile@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/heqile/http_testing',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
