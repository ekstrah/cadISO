from utils import Utils


class TestClass:
    image_src = "./src/tables"

    def test_mytest(
        self,
    ):
        assert len(Utils.get_all_files(self.image_src)) > 0
