from schematics.types import ModelType, StringType, PolyModelType, DictType, ListType

from spaceone.inventory.connector.aws_auto_scaling_connector.schema.data import AutoScalingGroup
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, BadgeDyField, DateTimeDyField, \
    EnumDyField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, ListDynamicLayout, \
    SimpleTableDynamicLayout
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
AUTO SCALING GROUP
'''

class AutoScalingResource(CloudServiceResource):
    cloud_service_group = StringType(default='AutoScaling')


class AutoScalingGroupResource(AutoScalingResource):
    cloud_service_type = StringType(default='AutoScalingGroup')
    data = ModelType(AutoScalingGroup)


class AutoScalingGroupResponse(CloudServiceResponse):
    resource = PolyModelType(AutoScalingGroupResource)



