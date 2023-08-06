from pygav.utils import rolling_window

from pygav.utils import Timer

def test_rolling_window():
    lst = list(range(20))
    assert list(rolling_window(lst, 3, 2))[2] == [4, 5, 6]

    lst = list(range(0))
    assert list(rolling_window(lst, 1, 1)) == []
