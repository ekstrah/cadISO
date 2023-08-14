import pytest
from utils.utils import plus


class TestClass:
    plus_value = 3

    def test_mytest(self,):
        assert self.plus_value == plus(1, 2)