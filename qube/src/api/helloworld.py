#!/usr/bin/python
"""
Add docstring here
"""
from flask_restful_swagger_2 import Resource, swagger
from flask_restful import reqparse
from qube.src.api.swagger_models.parameters import (
    header_ex, path_ex, query_ex, body_ex,
    body_post_ex, body_put_ex)
from qube.src.api.swagger_models.response_messages import (
    response_msgs, post_response_msgs, get_response_msgs,
    put_response_msgs, del_response_msgs, ErrorModel)
from qube.src.commons.log import Log as LOG
from flask import  request
from qube.src.models.hello import Hello
from qube.src.api.swagger_models.hello import *
from qube.src.commons.utils import clean_nonserializable_attributes
from qube.src.api.decorators import login_required
import json
from mongoalchemy.exceptions import DocumentException, MissingValueException, ExtraValueException, FieldNotRetrieved, BadFieldSpecification


hello_item_get_params = [header_ex, path_ex, query_ex]
hello_item_put_params = [header_ex, path_ex, body_put_ex]
hello_item_delete_params = [header_ex, path_ex]
hello_get_params = [header_ex]
hello_post_params = [header_ex, body_post_ex]


class HelloItemResource(Resource):
    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world get operation',
            'parameters': hello_item_get_params,
            'responses': get_response_msgs
        }
    )

    @login_required
    def get(self, id):
        """gets an hello item that omar has changed
        """
        LOG.debug("hello world")

        data = Hello.query.get(id)
        if data is None:
            return 'not found', 404

        hello_data = data.wrap()
        clean_nonserializable_attributes(hello_data)
        return HelloModel(**hello_data)

    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world put operation',
            'parameters': hello_item_put_params,
            'responses': put_response_msgs
        }
    )
    @login_required
    def put(self, id):
        """
        updates an hello item
        """
        try:
            hello_model = HelloModelPut(**request.get_json())
            hello_record = Hello.query.get(id) #Hello is a mongo class
            if hello_record is None:
                return 'not found', 404
            for key in hello_model:
                hello_record.__setattr__(key, hello_model[key])
            hello_record.save()
            return '', 204, {'Location': request.path + '/' + str(hello_record.mongo_id)}
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'message': e.args[0]}), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'message': ex.args[0]}), 500
    
    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world delete operation',
            'parameters': hello_item_delete_params,
            'responses': del_response_msgs
        }
    )
    @login_required
    def delete(self, id):
        """
        Delete hello item
        """
        try:
            hello = Hello.query.get(id)
            if hello is None:
                return 'not found', 404
            hello.remove()
            return '', 204
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'message': e.args[0]}), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'message': ex.args[0]}), 500

     
        return 'unexpected error', 500

class HelloWorld(Resource):
    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world get operation',
            'parameters': hello_get_params,
            'responses': get_response_msgs
        }
    )
    @login_required
    def get(self):
        """
        gets all hello items
        """
        LOG.debug("Serving  Get all request")
        hello_list = []
        data = Hello.query.all()
        #hello_data = service.wrap()
        for hello_data_item in data:
            hello_data = hello_data_item.wrap()
            clean_nonserializable_attributes(hello_data)
            hello_list.append(hello_data)
        #normalize the name for 'id'
        return hello_list
    

    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world create operation',
            'parameters' : hello_post_params,
            'responses': post_response_msgs
        }
    )
    @login_required
    def post(self):
        """
        Adds a hello item.
        """
        hello_data = None
        try:
            hello_model = HelloModelPost(**request.get_json())
            new_hello = Hello();
            for key in hello_model:
                new_hello.__setattr__(key, hello_model[key])
            hello_data = new_hello
            hello_data.save()
            return '', 201, {'Location': request.path + '/' + str(hello_data.mongo_id)}
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'message': e.args[0]}), 400
        except ExtraValueException as e:
            LOG.error(e)
            return ErrorModel(**{'message': "{} is not valid input".format(e.args[0]) }), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'message': ex.args[0]}), 500

