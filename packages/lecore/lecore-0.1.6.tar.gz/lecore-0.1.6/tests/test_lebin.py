import unittest
from time import sleep

try:
    import lecore.LeBin as LeBin
except ImportError:
    import src.lecore.LeBin as LeBin


class TestSimple(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Create instance of looger class
        """
        com = LeBin.SerialCom()
        cls.com = com
        cls.rm = LeBin.RegisterMap(com)

    def setUp(self) -> None:
        """
        Insert just some delay between tests
        """
        sleep(1)

    def test001_set_device(self):
        """
        Set identification of device we are sending data from
        """
        sleep(1)

    def test002_lebin_visual(self):
        vis = LeBin.VisualLeBin(self.rm)

        vis.draw(height=700)

        vis.handle()


if __name__ == '__main__':
    unittest.main()

