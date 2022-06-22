import pytest

@pytest.mark.parametrize("num_1, num_2, result", [(3,2,5),
                                                  (5,2,7),
                                                  (8,7,15)
                                                 ])
def test_add(num_1, num_2, result):
    total_sum = num_1 + num_2
    # True is ok (green), False will error (red)
    assert total_sum == result