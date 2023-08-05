# This file is placed in the Public Domain.
#
# pylama: ignore=E402,E302,E265,E303


import os
import sys
import unittest


sys.path.insert(0, "..")



from opr.objects import Object
from opr.persist import Persist, write


import opr.persist


Persist.workdir = '.test'


ATTRS1 = (
          'Persist',
          'last',
          'read',
          'write',
          'writerec'
         )


class TestStorage(unittest.TestCase):

    def test_constructor(self):
        obj = Persist()
        self.assertTrue(type(obj), Persist)

    def test__class(self):
        obj = Persist()
        clz = obj.__class__()
        self.assertTrue('Persist' in str(type(clz)))

    def test_dirmodule(self):
        self.assertEqual(
                         dir(opr.persist),
                         list(ATTRS1)
                        )

    def test_module(self):
        self.assertTrue(Persist().__module__, 'opr.persist')

    def test_save(self):
        Persist.workdir = '.test'
        obj = Object()
        opath = write(obj)
        self.assertTrue(os.path.exists(Persist.path(opath)))
