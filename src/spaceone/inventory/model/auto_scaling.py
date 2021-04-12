import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, FloatType, DateTimeType, serializable, ListType, \
    BooleanType, PolyModelType
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse

_LOGGER = logging.getLogger(__name__)

'''
AUTO SCALING GROUPS
'''
class LaunchTemplate(Model):
    launch_template_id = StringType(deserialize_from="LaunchTemplateId", serialize_when_none=False)
    launch_template_name = StringType(deserialize_from="LaunchTemplateName", serialize_when_none=False)
    version = StringType(deserialize_from="Version", serialize_when_none=False)


class AutoScalingGroupInstances(Model):
    instance_id = StringType(deserialize_from="InstanceId", serialize_when_none=False)
    instance_type = StringType(deserialize_from="InstanceType", serialize_when_none=False)
    availability_zone = StringType(deserialize_from="AvailabilityZone", serialize_when_none=False)
    lifecycle_state = StringType(deserialize_from="LifecycleState", serialize_when_none=False)
    lifecycle = StringType(choices=('spot', 'scheduled'), serialize_when_none=False)
    health_status = StringType(deserialize_from="HealthStatus", serialize_when_none=False)
    launch_configuration_name = StringType(deserialize_from="LaunchConfigurationName", serialize_when_none=False)
    launch_template = ModelType(LaunchTemplate, deserialize_from="LaunchTemplate", serialize_when_none=False)
    protected_from_scale_in = BooleanType(deserialize_from="ProtectedFromScaleIn", serialize_when_none=False)
    weighted_capacity = StringType(deserialize_from="WeightedCapacity", serialize_when_none=False)


class AutoScalingGroup(Model):
    auto_scaling_group_name = StringType(deserialize_from="AutoScalingGroupName")
    auto_scaling_group_arn = StringType(deserialize_from="AutoScalingGroupARN")
    min_size = IntType(deserialize_from="MinSize")
    max_size = IntType(deserialize_from="MaxSize")
    desired_capacity = IntType(deserialize_from="DesiredCapacity")
    instances = ListType(ModelType(AutoScalingGroupInstances), deserialize_from="Instances", default=[])

    def reference(self):
        return {
            "resource_id": self.auto_scaling_group_arn,
        }


class AutoScalingResource(CloudServiceResource):
    cloud_service_group = StringType(default='EC2')
    cloud_service_type = StringType(default='AutoScalingGroup')
    data = ModelType(AutoScalingGroup)


class AutoScalingResponse(CloudServiceResponse):
    resource = ModelType(AutoScalingResource)
