import time

from qube.src.commons.error import ErrorCodes, omartestpy2ServiceError
from qube.src.commons.utils import clean_nonserializable_attributes
from qube.src.models.omartestpy2 import omartestpy2


class omartestpy2Service:
    def __init__(self, context):
        self.auth_context = context

    def find_by_id(self, entity_id):
        # filter with id not working,
        # unable to proceed with tenant filter
        data = omartestpy2.query.get(entity_id)
        if data is None:
            raise omartestpy2ServiceError(
                'omartestpy2 {} not found'.format(entity_id),
                ErrorCodes.NOT_FOUND)

        data = data.wrap()
        clean_nonserializable_attributes(data)
        return data

    def get_all(self):
        list = []
        data = omartestpy2.query.filter(
            omartestpy2.tenantId == self.auth_context.tenant_id)
        for data_item in data:
            data = data_item.wrap()
            clean_nonserializable_attributes(data)
            list.append(data)
        return list

    def save(self, model):
        new_data = omartestpy2()
        for key in model:
            new_data.__setattr__(key, model[key])
        data = new_data
        data.tenantId = self.auth_context.tenant_id
        data.orgId = self.auth_context.org_id
        data.createdBy = self.auth_context.user_id
        data.createdDate = str(int(time.time()))
        data.modifiedBy = self.auth_context.user_id
        data.modifiedDate = str(int(time.time()))
        data.save()
        result = data.wrap()

        clean_nonserializable_attributes(result)
        return result

    def update(self, model, entity_id):

        record = omartestpy2.query.get(entity_id)  # omartestpy2 is a mongo class
        if record is None:
            raise omartestpy2ServiceError(
                'omartestpy2 {} not found'.format(entity_id),
                ErrorCodes.NOT_FOUND)

        for key in model:
            record.__setattr__(key, model[key])
        record.modifiedBy = self.auth_context.user_id
        record.modifiedDate = str(int(time.time()))
        record.save()
        result = record.wrap()
        clean_nonserializable_attributes(result)
        return result

    def delete(self, entity_id):
        if not self.auth_context.is_system_user:
            raise omartestpy2ServiceError(
                'Delete operation is forbidden',
                ErrorCodes.NOT_ALLOWED)
        data = omartestpy2.query.get(entity_id)
        if data is None:
            raise omartestpy2ServiceError(
                'omartestpy2 {} not found'.format(entity_id),
                ErrorCodes.NOT_FOUND)
        data.remove()
