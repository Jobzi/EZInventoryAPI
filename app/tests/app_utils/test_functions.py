import pytest
from app.utils import functions


@pytest.mark.parametrize('rejected_keys', [
    {'a', 'b'},
    ['c']
])
def test_filter_dict_keys(rejected_keys):
    initial_dict = {'a': 1, 'b': 2, 'c': 3}
    filtered_dict = functions.filter_dict_keys(initial_dict, rejected_keys)
    for key in rejected_keys:
        assert key not in filtered_dict
