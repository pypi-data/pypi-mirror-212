# This file is placed in the Public Domain.
#
# pylama: ignore=E402,E302,E265,E303,E231,E265


import sys
import unittest


sys.path.insert(0, "..")


from opr.encoder import dumps
from opr.objects import Object


VALIDJSON = '{"test": "bla"}'


class TestEncoder(unittest.TestCase):


    def test_dumps(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(dumps(obj), VALIDJSON)
