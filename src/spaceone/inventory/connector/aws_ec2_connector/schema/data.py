import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)

class Compute(Model):
    instance_state = StringType(deserialize_from="instance_state", choices=('PENDING', 'RUNNING', 'SHUTTING-DOWN', 'TERMINATED', 'STOPPING', 'STOPPED'))
    instance_id = StringType(deserialize_from="InstanceId")
    account = StringType(deserialize_from="account")

class AWS(Model):
    instance_status = StringType(deserialize_from='InstanceStatus', choices=('passed', 'failed', 'insufficient-data', 'initializing'), serialize_when_none=False)
    system_status = StringType(deserialize_from='SystemStatus', choices=('passed', 'failed', 'insufficient-data', 'initializing'), serialize_when_none=False)

class Server(Model):
    compute = ModelType(Compute, deserialize_from="Compute")
    power_state = ModelType(AWS, deserialize_from="aws")

    def reference(self, region_code):
        return {
                    "resource_id": self.compute.instance_id,
                    "external_link": f"https://{region_code}.console.aws.amazon.com/ec2/v2/home?region={region_code}#Instances:{self.compute.instance_id}"
                }

