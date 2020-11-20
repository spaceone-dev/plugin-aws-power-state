import logging
from spaceone.inventory.libs.connector import AWSConnector
from spaceone.inventory.error import *

__all__ = ['EC2Connector']
_LOGGER = logging.getLogger(__name__)


class EC2Connector(AWSConnector):
    service = 'ec2'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def describe_instance_status(self, **query):
        instances_status = []
        query = self.generate_query(is_paginate=True, **query)
        paginator = self.client.get_paginator('describe_instance_status')
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            instances_status.extend(data.get('InstanceStatuses', []))

        return instances_status

    def describe_instances(self, **query):
        instances = []
        query = self.generate_query(is_paginate=True, **query)
        paginator = self.client.get_paginator('describe_instances')
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            for reservation in data.get('Reservations', []):
                instances.extend(reservation.get('Instances', []))

        return instances