import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse

_LOGGER = logging.getLogger(__name__)


class RDS(Model):
    arn = StringType()
    db_identifier = StringType()
    status = StringType()
    role = StringType()

    def reference(self):
        return {
            "resource_id": self.arn,
        }


class RDSResource(CloudServiceResource):
    cloud_service_group = StringType(default='RDS')


class RDSDatabaseResource(RDSResource):
    cloud_service_type = StringType(default='Database')
    data = ModelType(RDS)


class RDSInstanceResource(RDSResource):
    cloud_service_type = StringType(default='Instance')
    data = ModelType(RDS)


class RDSDatabaseResponse(CloudServiceResponse):
    resource = ModelType(RDSDatabaseResource)


class RDSInstanceResponse(CloudServiceResponse):
    resource = ModelType(RDSInstanceResource)
