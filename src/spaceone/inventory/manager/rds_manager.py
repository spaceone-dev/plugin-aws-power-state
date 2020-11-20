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

            for cluster in rds_conn.describe_db_clusters():
                cluster = Cluster(cluster, strict=False)

                db = {
                    'arn': cluster.db_cluster_arn,
                    'db_identifier': cluster.db_cluster_identifier,
                    'status': cluster.status,
                    'role': 'cluster'
                }

                db_data = Database(db, strict=False)

                rds_resource = RDSResource({
                    'data': db_data,
                    'reference': ReferenceModel(db_data.reference())
                })

                resources.append(RDSResponse({'resource': rds_resource}))

            for instance in rds_conn.describe_db_instances():
                instance = Instance(instance, strict=False)

                db = {
                    'arn': instance.db_instance_arn,
                    'db_identifier': instance.db_instance_identifier,
                    'status': instance.db_instance_status,
                    'role': 'instance'
                }

                db_data = Database(db, strict=False)

                rds_resource = RDSResource({
                    'data': db_data,
                    'reference': ReferenceModel(db_data.reference())
                })

                resources.append(RDSResponse({'resource': rds_resource}))

        print(f' RDS Finished {time.time() - start_time} Seconds')
        return resources
