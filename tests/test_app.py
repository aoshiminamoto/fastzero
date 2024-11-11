import pytest


@pytest.fixture(params=list(range(5)))
def param_loop(request):
    return request.param


def test_something(param_loop):
    print(param_loop)
    return True
