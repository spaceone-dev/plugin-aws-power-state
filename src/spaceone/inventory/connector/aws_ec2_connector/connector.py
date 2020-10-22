import time
import logging
from typing import List

from spaceone.inventory.connector.aws_ec2_connector.schema.data import Server
from spaceone.inventory.connector.aws_ec2_connector.schema.resource import ServerResource, ServerResponse
from spaceone.inventory.connector.aws_ec2_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class EC2Connector(SchematicAWSConnector):
    service_name = 'ec2'
    function_response_schema = ServerResponse

    def get_resources(self) -> List[ServerResource]:
        print("** EC2 Manager START **")
        resources = []
        start_time = time.time()

        collect_resource = {
            'request_method': self.request_instance_status,
            'resource': ServerResource,
            'response_schema': ServerResponse
        }

        for region_name in self.region_names:
            self.reset_region(region_name)
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        print(f' EC2 Finished {time.time() - start_time} Seconds')
        return resources

    def request_instance_status(self, region_name) -> List[Server]:
        # Get Instances status
        # WARNING: 
        # STOPPED instance is not listed at describe_instance_status
        paginator = self.client.get_paginator('describe_instance_status')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        count = 0
        for data in response_iterator:
            for raw in data.get('InstanceStatuses', []):
                raw.update({
                    'aws': {
                        'PowerStatus': self._get_power_status(raw),
                    },
                    'compute': self._get_compute(raw),
                    'instance_id': raw['InstanceId']
                })
                count += 1
                yield Server(raw, strict=False)

        # STOPPED instance is not listed at describe_instance_status
        paginator = self.client.get_paginator('describe_instances')
        response_iterator = paginator.paginate(
            Filters = [
                {'Name': 'instance-state-name', 'Values': ['stopped']}
            ],
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for reservation in data.get('Reservations', []):
                for raw in reservation.get('Instances', []):
                    instance_data = {}
                    instance_data.update({
                        'aws': {
                            'PowerStatus': 'STOPPED'
                        },
                        'compute': self._get_compute2(raw),
                        'instance_id': raw['InstanceId']
                    })
                    count += 1
                    yield Server(instance_data, strict=False)

        print(f"{region_name} ec2: {count}")

    def _get_power_status(self, InstanceStatuses):
        """ Based on InstanceStatus,
        possible: RUNNING | UNHEALTHY
        """
        ins_status = self._get_status(InstanceStatuses['InstanceStatus'])
        sys_status = self._get_status(InstanceStatuses['SystemStatus'])
        if ins_status == 'passed' and sys_status == 'passed':
            return 'RUNNING'
        return 'UNHEALTHY'

    @staticmethod
    def _get_status(InstanceStatus):
        details = InstanceStatus.get('Details', [])
        for detail in details:
            name = detail.get('Name', None)
            if name == "reachability":
                return detail.get('Status', None)
        return None

    def _get_compute(self, InstanceStatus):
        return {
            'instance_id': InstanceStatus['InstanceId'],
            'account': self.account_id,
            'instance_state': (InstanceStatus['InstanceState']['Name']).upper()
        }

    # parse from describe_instances
    def _get_compute2(self, Instance):
        return {
            'instance_id': Instance['InstanceId'],
            'account': self.account_id,
            'instance_state': 'STOPPED'
        }

