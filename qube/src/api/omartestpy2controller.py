#!/usr/bin/python
"""
Add docstring here
"""
from flask import request
from flask_restful_swagger_2 import Resource, swagger
from mongoalchemy.exceptions import ExtraValueException

from qube.src.api.decorators import login_required
from qube.src.api.swagger_models.omartestpy2 import omartestpy2Model # noqa: ignore=I100
from qube.src.api.swagger_models.omartestpy2 import omartestpy2ModelPost # noqa: ignore=I100
from qube.src.api.swagger_models.omartestpy2 import omartestpy2ModelPostResponse # noqa: ignore=I100
from qube.src.api.swagger_models.omartestpy2 import omartestpy2ModelPut # noqa: ignore=I100

from qube.src.api.swagger_models.parameters import (
    body_post_ex, body_put_ex, header_ex, path_ex, query_ex)
from qube.src.api.swagger_models.response_messages import (
    del_response_msgs, ErrorModel, get_response_msgs, post_response_msgs,
    put_response_msgs)
from qube.src.commons.error import omartestpy2ServiceError
from qube.src.commons.log import Log as LOG
from qube.src.commons.utils import clean_nonserializable_attributes
from qube.src.services.omartestpy2service import omartestpy2Service

EMPTY = ''
get_details_params = [header_ex, path_ex, query_ex]
put_params = [header_ex, path_ex, body_put_ex]
delete_params = [header_ex, path_ex]
get_params = [header_ex]
post_params = [header_ex, body_post_ex]


class omartestpy2ItemController(Resource):
    @swagger.doc(
        {
            'tags': ['omartestpy2'],
            'description': 'omartestpy2 get operation',
            'parameters': get_details_params,
            'responses': get_response_msgs
        }
    )
    @login_required
    def get(self, authcontext, entity_id):
        """gets an omartestpy2 item that omar has changed
        """
        try:
            LOG.debug("Get details by id %s ", entity_id)
            data = omartestpy2Service(authcontext['context'])\
                .find_by_id(entity_id)
            clean_nonserializable_attributes(data)
        except omartestpy2ServiceError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': str(e.errors.value),
                                 'error_message': e.args[0]}), e.errors
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': '400',
                                 'error_message': e.args[0]}), 400
        return omartestpy2Model(**data), 200

    @swagger.doc(
        {
            'tags': ['omartestpy2'],
            'description': 'omartestpy2 put operation',
            'parameters': put_params,
            'responses': put_response_msgs
        }
    )
    @login_required
    def put(self, authcontext, entity_id):
        """
        updates an omartestpy2 item
        """
        try:
            model = omartestpy2ModelPut(**request.get_json())
            context = authcontext['context']
            omartestpy2Service(context).update(model, entity_id)
            return EMPTY, 204
        except omartestpy2ServiceError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': str(e.errors.value),
                                 'error_message': e.args[0]}), e.errors
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': '400',
                                 'error_message': e.args[0]}), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'error_code': '500',
                                 'error_message': ex.args[0]}), 500

    @swagger.doc(
        {
            'tags': ['omartestpy2'],
            'description': 'omartestpy2 delete operation',
            'parameters': delete_params,
            'responses': del_response_msgs
        }
    )
    @login_required
    def delete(self, authcontext, entity_id):
        """
        Delete omartestpy2 item
        """
        try:
            omartestpy2Service(authcontext['context']).delete(entity_id)
            return EMPTY, 204
        except omartestpy2ServiceError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': str(e.errors.value),
                                 'error_message': e.args[0]}), e.errors
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': '400',
                                 'error_message': e.args[0]}), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'error_code': '500',
                                 'error_message': ex.args[0]}), 500


class omartestpy2Controller(Resource):
    @swagger.doc(
        {
            'tags': ['omartestpy2'],
            'description': 'omartestpy2 get operation',
            'parameters': get_params,
            'responses': get_response_msgs
        }
    )
    @login_required
    def get(self, authcontext):
        """
        gets all omartestpy2 items
        """
        LOG.debug("Serving  Get all request")
        list = omartestpy2Service(authcontext['context']).get_all()
        # normalize the name for 'id'
        return list, 200

    @swagger.doc(
        {
            'tags': ['omartestpy2'],
            'description': 'omartestpy2 create operation',
            'parameters': post_params,
            'responses': post_response_msgs
        }
    )
    @login_required
    def post(self, authcontext):
        """
        Adds a omartestpy2 item.
        """
        try:
            model = omartestpy2ModelPost(**request.get_json())
            result = omartestpy2Service(authcontext['context'])\
                .save(model)

            response = omartestpy2ModelPostResponse()
            for key in response.properties:
                response[key] = result[key]

            return (response, 201,
                    {'Location': request.path + '/' + str(response['id'])})
        except ValueError as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': str(e.errors.value),
                                 'error_message': e.args[0]}), 400
        except ExtraValueException as e:
            LOG.error(e)
            return ErrorModel(**{'error_code': '400',
                                 'error_message': "{} is not valid input".
                              format(e.args[0])}), 400
        except Exception as ex:
            LOG.error(ex)
            return ErrorModel(**{'error_code': '500',
                                 'error_message': ex.args[0]}), 500
