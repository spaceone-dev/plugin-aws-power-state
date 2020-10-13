import time
import logging
from typing import List

from spaceone.inventory.connector.aws_auto_scaling_connector.schema.data import AutoScalingGroup
from spaceone.inventory.connector.aws_auto_scaling_connector.schema.resource import AutoScalingGroupResource, \
    AutoScalingGroupResponse
from spaceone.inventory.connector.aws_auto_scaling_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class AutoScalingConnector(SchematicAWSConnector):
    _launch_configurations = None
    _launch_templates = None

    service_name = 'autoscaling'

    def get_resources(self):
        print("** Auto Scaling Start **")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.request_auto_scaling_group_data,
                'resource': AutoScalingGroupResource,
                'response_schema': AutoScalingGroupResponse
            }
        ]

        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            # print(f'[ AutoScaling {region_name} ]')
            self._launch_configurations = []
            self._launch_templates = []
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' Auto Scaling Finished {time.time() - start_time} Seconds')
        return resources

    def request_auto_scaling_group_data(self, region_name) -> List[AutoScalingGroup]:
        paginator = self.client.get_paginator('describe_auto_scaling_groups')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('AutoScalingGroups', []):
                res = AutoScalingGroup(raw, strict=False)
                yield res

