import time
import logging
from typing import List

from spaceone.inventory.connector.aws_rds_connector.schema.data import Database, Cluster, Instance
from spaceone.inventory.connector.aws_rds_connector.schema.resource import DatabaseResource, DatabaseResponse, \
    DBClusterResource, DBInstanceResource
from spaceone.inventory.connector.aws_rds_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector


_LOGGER = logging.getLogger(__name__)
RDS_FILTER = ['aurora', 'aurora-mysql', 'mysql', 'mariadb', 'postgres',
              'oracle-ee', 'oracle-se', 'oracle-se1', 'oracle-se2',
              'sqlserver-ex', 'sqlserver-web', 'sqlserver-se', 'sqlserver-ee']


class RDSConnector(SchematicAWSConnector):
    service_name = 'rds'

    def get_resources(self):
        print("** RDS START **")
        resources = []
        start_time = time.time()

        collect_resources = [
            {
                'request_method': self.db_cluster_data,
                'resource': DBClusterResource,
                'response_schema': DatabaseResponse
            },
            {
                'request_method': self.db_instance_data,
                'resource': DBInstanceResource,
                'response_schema': DatabaseResponse
            }
        ]

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        for region_name in self.region_names:
            # print(f'[ {region_name} ]')
            self.reset_region(region_name)

            for collect_resource in collect_resources:
                resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' RDS Finished {time.time() - start_time} Seconds')
        return resources

    def db_instance_data(self, region_name) -> List[Database]:
        for instance in self.describe_instances():
            db = {
                'arn': instance.db_instance_arn,
                'db_identifier': instance.db_instance_identifier,
                'status': instance.db_instance_status,
                'role': 'instance'
            }
            yield Database(db, strict=False)

    def db_cluster_data(self, region_name) -> List[Database]:
        for cluster in self.describe_clusters():
            db = {
                'arn': cluster.db_cluster_arn,
                'db_identifier': cluster.db_cluster_identifier,
                'status': cluster.status,
                'role': 'cluster'
            }
            yield Database(db, strict=False)

    def describe_clusters(self) -> List[Cluster]:
        paginator = self.client.get_paginator('describe_db_clusters')
        response_iterator = paginator.paginate(
            Filters=[
                {
                    'Name': 'engine',
                    'Values': RDS_FILTER
                },
            ],
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBClusters', []):
                res = Cluster(raw, strict=False)
                yield res

    def describe_instances(self) -> List[Instance]:
        paginator = self.client.get_paginator('describe_db_instances')
        response_iterator = paginator.paginate(
            Filters=[
                {
                    'Name': 'engine',
                    'Values': RDS_FILTER
                },
            ],
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('DBInstances', []):
                yield Instance(raw, strict=False)

