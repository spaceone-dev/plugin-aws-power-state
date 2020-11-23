import logging
from spaceone.inventory.libs.connector import AWSConnector
from spaceone.inventory.error import *

__all__ = ['RDSConnector']
_LOGGER = logging.getLogger(__name__)


class RDSConnector(AWSConnector):

    service = 'rds'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def describe_db_clusters(self, **query):
        clusters = []

        query = self.generate_query(is_paginate=True, **query)
        paginator = self.client.get_paginator('describe_db_clusters')
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            clusters.extend(data.get('DBClusters', []))

        return clusters

    def describe_db_instances(self, **query):
        instances = []

        query = self.generate_query(is_paginate=True, **query)
        paginator = self.client.get_paginator('describe_db_instances')
        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            instances.extend(data.get('DBInstances', []))

        return instances
