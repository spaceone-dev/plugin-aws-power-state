import logging

from schematics import Model
from schematics.types import ModelType, StringType, ListType, DictType
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse

_LOGGER = logging.getLogger(__name__)

'''
EC2
'''
class Compute(Model):
    instance_state = StringType(deserialize_from="instance_state", choices=('PENDING', 'RUNNING', 'SHUTTING-DOWN',
                                                                            'TERMINATED', 'STOPPING', 'STOPPED'))
    instance_id = StringType(deserialize_from="InstanceId")
    account = StringType(deserialize_from="account")


class PowerState(Model):
    status = StringType(deserialize_from='PowerStatus', choices=('RUNNING', 'STOPPED', 'UNHEALTHY'),
                        serialize_when_none=False)


class Server(Model):
    compute = ModelType(Compute, deserialize_from="Compute")
    power_state = ModelType(PowerState, deserialize_from="aws")

    def reference(self):
        return {
            "resource_id": self.compute.instance_id,
        }


class EC2Resource(CloudServiceResource):
    cloud_service_group = StringType(default='EC2')
    cloud_service_type = StringType(default='Instance')
    data = ModelType(Server)


class EC2Response(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={'1': ['reference.resource_id']})
    resource_type = StringType(default='inventory.Server')
    resource = ModelType(EC2Resource)
