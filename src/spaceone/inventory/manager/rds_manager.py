import time
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.libs.manager import AWSPowerStateManager
from spaceone.inventory.connector.rds import RDSConnector
from spaceone.inventory.model.rds import *


class RDSManager(AWSPowerStateManager):
    connector_name = 'RDSConnector'

    def collect_power_state(self, params):
        print("** RDS Start **")
        start_time = time.time()
        rds_conn: RDSConnector = self.locator.get_connector(self.connector_name, **params)

        resources = []
        for region_name in params.get('regions', []):
            # print(f'[ RDS {region_name} ]')
            rds_conn.set_client(region_name)

            resources.extend(self.get_rds_databases(rds_conn))
            resources.extend(self.get_rds_instances(rds_conn))

        print(f' RDS Finished {time.time() - start_time} Seconds')
        return resources

    def get_rds_databases(self, rds_conn):
        databases = []
        for cluster in rds_conn.describe_db_clusters(Filters=self.get_rds_filter()):
            rds_cluster = {
                'arn': cluster['DBClusterArn'],
                'db_identifier': cluster['DBClusterIdentifier'],
                'status': cluster['Status'],
                'role': 'cluster'
            }

            rds_data = RDS(rds_cluster, strict=False)

            rds_resource = RDSDatabaseResource({
                'data': rds_data,
                'reference': ReferenceModel(rds_data.reference())
            })

            databases.append(RDSDatabaseResponse({'resource': rds_resource}))

        for instance in rds_conn.describe_db_instances(Filters=self.get_rds_filter()):
            if not instance.get('DBClusterIdentifier'):
                rds_instance = {
                    'arn': instance['DBInstanceArn'],
                    'db_identifier': instance['DBInstanceIdentifier'],
                    'status': instance['DBInstanceStatus'],
                    'role': 'instance'
                }

                rds_data = RDS(rds_instance, strict=False)

                rds_resource = RDSDatabaseResource({
                    'data': rds_data,
                    'reference': ReferenceModel(rds_data.reference())
                })

                databases.append(RDSDatabaseResponse({'resource': rds_resource}))

        return databases

    def get_rds_instances(self, rds_conn):
        instances = []
        for instance in rds_conn.describe_db_instances(Filters=self.get_rds_filter()):
            rds = {
                'arn': instance['DBInstanceArn'],
                'db_identifier': instance['DBInstanceIdentifier'],
                'status': instance['DBInstanceStatus'],
                'role': 'instance'
            }

            rds_data = RDS(rds, strict=False)

            rds_resource = RDSInstanceResource({
                'data': rds_data,
                'reference': ReferenceModel(rds_data.reference())
            })

            instances.append(RDSInstanceResponse({'resource': rds_resource}))

        return instances

    @staticmethod
    def get_rds_filter():
        RDS_FILTER = ['aurora', 'aurora-mysql', 'mysql', 'mariadb', 'postgres',
                      'oracle-ee', 'oracle-se', 'oracle-se1', 'oracle-se2',
                      'sqlserver-ex', 'sqlserver-web', 'sqlserver-se', 'sqlserver-ee']

        return [{
            'Name': 'engine',
            'Values': RDS_FILTER
        }]
