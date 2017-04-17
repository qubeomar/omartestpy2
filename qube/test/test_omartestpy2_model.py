#!/usr/bin/python
"""
Add docstring here
"""
import time
import unittest

import mock

from mock import patch
import mongomock


class Testomartestpy2Model(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_omartestpy2_model(self):
        from qube.src.models.omartestpy2 import omartestpy2
        omartestpy2_data = omartestpy2(name='testname')
        omartestpy2_data.tenantId = "23432523452345"
        omartestpy2_data.orgId = "987656789765670"
        omartestpy2_data.createdBy = "1009009009988"
        omartestpy2_data.modifiedBy = "1009009009988"
        omartestpy2_data.createDate = str(int(time.time()))
        omartestpy2_data.modifiedDate = str(int(time.time()))
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            omartestpy2_data.save()
            self.assertIsNotNone(omartestpy2_data.mongo_id)
            omartestpy2_data.remove()

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()
