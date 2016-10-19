from brown.utils import numbers

def test_clamp_value():
    assert(numbers.clamp_value(-50, 3, 5) == 3)
    assert(numbers.clamp_value(3, 3, 5) == 3)
    assert(numbers.clamp_value(4, 3, 5) == 4)
    assert(numbers.clamp_value(5, 3, 5) == 5)
    assert(numbers.clamp_value(50, 3, 5) == 5)
