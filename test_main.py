from utils import Utils


class TestClass:
    plus_value = 3

    def test_mytest(
        self,
    ):
        assert self.plus_value == Utils.plus(1, 2)
