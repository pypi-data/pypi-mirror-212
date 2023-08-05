import unittest
from dxitemspy.dxitems import DXIEngine


class TestDXIEngine(unittest.TestCase):

    def test_dxipy(self):
        de = DXIEngine()

        out = de.get_dxi(["A00"])
        self.assertTrue("INF" in out["labels"])

        out = de.get_dxi(["I10"])
        self.assertTrue("DXI1_CIR002" in out["labels"])

        out = de.get_dxi(["A00", "I10"])
        self.assertTrue(len(out["labels"])==7)



