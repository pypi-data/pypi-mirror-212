# This file is placed in the Public Domain.
# pylint: disable=C0114,C0115,C0116,C0413,E1101,R1732
# pylama: ignore=W0611,E265,E402


import sys
import unittest


sys.path.insert(0, "..")


from opr.objects import Object
from opr.persist import read, write


class TestComposite(unittest.TestCase):

    def testcomposite(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        self.assertEqual(obj.obj.a, "test")

    def testcompositeprint(self):
        obj = Object()
        obj.obj = Object()
        obj.obj.a = "test"
        pth = write(obj)
        ooo = Object()
        read(ooo, pth)
        #self.assertEqual(ooo.obj.a, "test")
        self.assertTrue(ooo.obj)
