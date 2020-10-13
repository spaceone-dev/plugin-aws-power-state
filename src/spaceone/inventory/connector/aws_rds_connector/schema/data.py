import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)

'''
INSTANCE
'''

class Instance(Model):
    db_instance_identifier = StringType(deserialize_from="DBInstanceIdentifier")
    db_instance_status = StringType(deserialize_from="DBInstanceStatus")
    db_instance_arn = StringType(deserialize_from="DBInstanceArn")

class Cluster(Model):
    status = StringType(deserialize_from="Status")
    db_cluster_arn = StringType(deserialize_from="DBClusterArn")
    db_cluster_identifier = StringType(deserialize_from="DBClusterIdentifier")

class Database(Model):
    arn = StringType()
    db_identifier = StringType()
    status = StringType()
    role = StringType()

    def reference(self, region_code):
        is_cluster = 'true' if self.role == 'cluster' else 'false'
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/rds/home?region={region_code}#database:id={self.db_identifier};is-cluster={is_cluster}"
        }

