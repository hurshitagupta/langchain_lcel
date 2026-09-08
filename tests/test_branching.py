import pytest

from branching.branching import is_maths, Classify
from guards import validate_input


def test_maths_classification():
    data = {
        "q": "what is 2+2",
        "classification": Classify(classification="maths")
    }

    assert is_maths(data) is True


def test_prose_classification():
    data = {
        "q": "what is LCEL",
        "classification": Classify(classification="prose")
    }

    assert is_maths(data) is False


def test_invalid_input():
    with pytest.raises(ValueError):
        validate_input({})