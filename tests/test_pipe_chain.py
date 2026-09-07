import pytest
from pipe_chain.pipe_chain import validate_input, validate_output


def test_valid_input():
    data = {"q": "What is LCEL?"}

    result = validate_input(data)

    assert result == data


def test_missing_question():
    with pytest.raises(ValueError):
        validate_input({})


def test_valid_output():
    output = "LCEL is used to compose LangChain runnables."

    result = validate_output(output)

    assert result == output


def test_invalid_output():
    with pytest.raises(ValueError):
        validate_output("")