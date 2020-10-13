from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_rds_connector.schema.data import Database
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, EnumDyField, \
    DateTimeDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout

class RDSResource(CloudServiceResource):
    cloud_service_group = StringType(default='RDS')


class DatabaseResource(RDSResource):
    cloud_service_type = StringType(default='Database')
    data = ModelType(Database)


class DBInstanceResource(DatabaseResource):
    pass

class DBClusterResource(DatabaseResource):
    pass

class DatabaseResponse(CloudServiceResponse):
    resource = PolyModelType([DBInstanceResource, DBClusterResource])

