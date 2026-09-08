import pytest

from failure_paths.failure_paths import primary_model, chain


def test_primary_failure():
    with pytest.raises(ValueError):
        primary_model({"q": "Hello"})


def test_retry_and_fallback():
    result = chain.invoke({"q": "Hello"})

    assert result == "Fallback model succeeded"