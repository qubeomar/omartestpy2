#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['OMARTESTPY2_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['OMARTESTPY2_MONGOALCHEMY_SERVER'] = ''
    os.environ['OMARTESTPY2_MONGOALCHEMY_PORT'] = ''
    os.environ['OMARTESTPY2_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.omartestpy2 import omartestpy2
    from qube.src.services.omartestpy2service import omartestpy2Service
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import ErrorCodes, omartestpy2ServiceError


class Testomartestpy2Service(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "tenantname",
                              "987656789765670", "orgname", "1009009009988",
                              "username", False)
        self.omartestpy2Service = omartestpy2Service(context)
        self.omartestpy2_api_model = self.createTestModelData()
        self.omartestpy2_data = self.setupDatabaseRecords(self.omartestpy2_api_model)
        self.omartestpy2_someoneelses = \
            self.setupDatabaseRecords(self.omartestpy2_api_model)
        self.omartestpy2_someoneelses.tenantId = "123432523452345"
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.omartestpy2_someoneelses.save()
        self.omartestpy2_api_model_put_description \
            = self.createTestModelDataDescription()
        self.test_data_collection = [self.omartestpy2_data]

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            for item in self.test_data_collection:
                item.remove()
            self.omartestpy2_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'description': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self, omartestpy2_api_model):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            omartestpy2_data = omartestpy2(name='test_record')
            for key in omartestpy2_api_model:
                omartestpy2_data.__setattr__(key, omartestpy2_api_model[key])

            omartestpy2_data.description = 'my short description'
            omartestpy2_data.tenantId = "23432523452345"
            omartestpy2_data.orgId = "987656789765670"
            omartestpy2_data.createdBy = "1009009009988"
            omartestpy2_data.modifiedBy = "1009009009988"
            omartestpy2_data.createDate = str(int(time.time()))
            omartestpy2_data.modifiedDate = str(int(time.time()))
            omartestpy2_data.save()
            return omartestpy2_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_omartestpy2(self, *args, **kwargs):
        result = self.omartestpy2Service.save(self.omartestpy2_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.omartestpy2_api_model['name'])
        omartestpy2.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_omartestpy2(self, *args, **kwargs):
        self.omartestpy2_api_model['name'] = 'modified for put'
        id_to_find = str(self.omartestpy2_data.mongo_id)
        result = self.omartestpy2Service.update(
            self.omartestpy2_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.omartestpy2_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_omartestpy2_description(self, *args, **kwargs):
        self.omartestpy2_api_model_put_description['description'] =\
            'modified for put'
        id_to_find = str(self.omartestpy2_data.mongo_id)
        result = self.omartestpy2Service.update(
            self.omartestpy2_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['description'] ==
                        self.omartestpy2_api_model_put_description['description'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_omartestpy2_item(self, *args, **kwargs):
        id_to_find = str(self.omartestpy2_data.mongo_id)
        result = self.omartestpy2Service.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_omartestpy2_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(omartestpy2ServiceError):
            self.omartestpy2Service.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_omartestpy2_list(self, *args, **kwargs):
        result_collection = self.omartestpy2Service.get_all()
        self.assertTrue(len(result_collection) == 1,
                        "Expected result 1 but got {} ".
                        format(str(len(result_collection))))
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.omartestpy2_data.mongo_id))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_not_system_user(self, *args, **kwargs):
        id_to_delete = str(self.omartestpy2_data.mongo_id)
        with self.assertRaises(omartestpy2ServiceError) as ex:
            self.omartestpy2Service.delete(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_ALLOWED)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_by_system_user(self, *args, **kwargs):
        id_to_delete = str(self.omartestpy2_data.mongo_id)
        self.omartestpy2Service.auth_context.is_system_user = True
        self.omartestpy2Service.delete(id_to_delete)
        with self.assertRaises(omartestpy2ServiceError) as ex:
            self.omartestpy2Service.find_by_id(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_FOUND)
        self.omartestpy2Service.auth_context.is_system_user = False

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_item_someoneelse(self, *args, **kwargs):
        id_to_delete = str(self.omartestpy2_someoneelses.mongo_id)
        with self.assertRaises(omartestpy2ServiceError):
            self.omartestpy2Service.delete(id_to_delete)
