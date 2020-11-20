import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, FloatType, DateTimeType, serializable, ListType, \
    BooleanType, PolyModelType
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse

_LOGGER = logging.getLogger(__name__)

'''
AUTO SCALING GROUPS
'''
class AutoScalingGroup(Model):
    auto_scaling_group_name = StringType(deserialize_from="AutoScalingGroupName")
    auto_scaling_group_arn = StringType(deserialize_from="AutoScalingGroupARN")
    min_size = IntType(deserialize_from="MinSize")
    max_size = IntType(deserialize_from="MaxSize")
    desired_capacity = IntType(deserialize_from="DesiredCapacity")

    def reference(self):
        return {
            "resource_id": self.auto_scaling_group_arn,
        }


class AutoScalingResource(CloudServiceResource):
    data = ModelType(AutoScalingGroup)


class AutoScalingResponse(CloudServiceResponse):
    resource = ModelType(AutoScalingResource)
