import pytest

from configurability.configurability import configurable_model
from guards import validate_input


def test_configurable_fields_exist():

    specs = configurable_model.config_specs

    ids = [spec.id for spec in specs]

    assert "model_name" in ids
    assert "temperature" in ids


def test_invalid_input():

    with pytest.raises(ValueError):
        validate_input({})