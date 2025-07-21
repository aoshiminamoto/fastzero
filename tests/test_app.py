import pytest


@pytest.fixture(params=list(range(5)))
def param_loop(request):
    return request.param


def test_something(param_loop):
    print(param_loop)
    assert True


def test_exception():
    with pytest.raises(Exception, match="Ocorrencia de Exception.") as exc:
        raise Exception("Ocorrencia de Exception.")

    assert "Ocorrencia de Exception." in str(exc.value)
