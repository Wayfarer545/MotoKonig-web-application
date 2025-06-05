import pytest

from app.domain.value_objects.pin_code import PinCode


def test_valid_pin():
    pin = PinCode("1234")
    assert str(pin) == "1234"


@pytest.mark.parametrize("pin", ["abc", "123", "1234567"])
def test_invalid_pin(pin):
    with pytest.raises(ValueError):
        PinCode(pin)
