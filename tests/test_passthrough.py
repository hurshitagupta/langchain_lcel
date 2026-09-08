import pytest

from passthrough.passthrough import chain


def test_passthrough_success():
    result = chain.invoke(
        {"q": "What is LCEL in LangChain?"}
    )

    assert result["q"] == "What is LCEL in LangChain?"
    assert result["word_count"] == 5


def test_passthrough_failure():
    with pytest.raises(ValueError):
        chain.invoke({})