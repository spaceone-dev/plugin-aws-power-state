import logging
from spaceone.inventory.libs.connector import AWSConnector
from spaceone.inventory.error import *


__all__ = ['AutoScalingConnector']
_LOGGER = logging.getLogger(__name__)


class AutoScalingConnector(AWSConnector):
    service = 'autoscaling'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def describe_auto_scaling_groups(self, **query):
        auto_scaling_groups = []
        query = self.generate_query(is_paginate=True, **query)

        paginator = self.client.get_paginator('describe_auto_scaling_groups')
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            auto_scaling_groups.extend(data.get('AutoScalingGroups', []))

        return auto_scaling_groups
