import unittest
from time import sleep

try:
    import lecore.VisualModbus as VM
except ImportError:
    import src.lecore.VisualModbus as VM


class TestSimple(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Create instance of looger class
        """
        mb = VM.MbClient.MbClient()
        cls.mb = mb
        cls.reg = VM.RegMap.RegMap(mb, slave=1)

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


if __name__ == '__main__':
    unittest.main()

