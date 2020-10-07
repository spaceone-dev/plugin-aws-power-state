from schematics import Model
from schematics.types import DictType, ListType, ModelType, PolyModelType, StringType
from spaceone.inventory.libs.schema.resource import BaseResponse, ReferenceModel
from spaceone.inventory.connector.aws_ec2_connector.schema.data import Server

class ServerResource(Model):
    data = ModelType(Server)
    reference = ModelType(ReferenceModel)

class ServerResponse(BaseResponse):
    match_rules = DictType(ListType(StringType), default={
        '1': ['reference.resource_id']
    })
    resource_type = StringType(default='inventory.Server')
    resource = PolyModelType(ServerResource)
    options = DictType(StringType, default={
        'update_mode': 'MERGE'})

