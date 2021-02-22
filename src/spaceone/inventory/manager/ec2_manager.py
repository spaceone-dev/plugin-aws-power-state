import time
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.libs.manager import AWSPowerStateManager
from spaceone.inventory.connector.ec2 import EC2Connector
from spaceone.inventory.model.ec2 import *



class EC2Manager(AWSPowerStateManager):
    connector_name = 'EC2Connector'

    def collect_power_state(self, params):
        # Get Instances status
        # WARNING:
        # STOPPED instance is not listed at describe_instance_status
        print("** EC2 Start **")
        start_time = time.time()
        ec2_conn: EC2Connector = self.locator.get_connector(self.connector_name, **params)
        account_id = params['account_id']

        resources = []
        for region_name in params.get('regions', []):
            # print(f'[ EC2 {region_name} ]')
            ec2_conn.set_client(region_name)

            for instance_status in ec2_conn.describe_instance_status():
                instance_status.update({
                    'aws': {
                        'PowerStatus': self._get_power_status(instance_status),
                    },
                    'compute': {
                        'instance_id': instance_status['InstanceId'],
                        'account': account_id,
                        'instance_state': (instance_status['InstanceState']['Name']).upper()
                    },
                    'instance_id': instance_status['InstanceId']
                })

                ec2_data = Server(instance_status, strict=False)

                ec2_resource = EC2Resource({
                    'data': ec2_data,
                    'reference': ReferenceModel(ec2_data.reference())
                })

                resources.append(EC2Response({'resource': ec2_resource}))

            # STOPPED instance is not listed at describe_instance_status
            instances = ec2_conn.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
            for instance in instances:
                instance_data = {}
                instance_data.update({
                    'aws': {
                        'PowerStatus': 'STOPPED'
                    },
                    'compute': {
                        'instance_id': instance['InstanceId'],
                        'account': account_id,
                        'instance_state': 'STOPPED'
                    },
                    'instance_id': instance['InstanceId']
                })

                ec2_data = Server(instance_data, strict=False)

                ec2_resource = EC2Resource({
                    'data': ec2_data,
                    'reference': ReferenceModel(ec2_data.reference())
                })

                resources.append(EC2Response({'resource': ec2_resource}))

            print(f"{region_name} ec2: {len(resources)}")

        print(f' EC2 Finished {time.time() - start_time} Seconds')
        return resources

    def _get_power_status(self, instance_statuses):
        """ Based on InstanceStatus,
        possible: RUNNING | UNHEALTHY | INITIALIZING
        """
        ins_status = self._get_status(instance_statuses['InstanceStatus'])
        sys_status = self._get_status(instance_statuses['SystemStatus'])
        if ins_status == 'passed' and sys_status == 'passed':
            return 'RUNNING'
        elif ins_status == 'initializing' or sys_status == 'initializing':
            return 'INITIALIZING'
        return 'UNHEALTHY'

    @staticmethod
    def _get_status(instance_status):
        details = instance_status.get('Details', [])
        for detail in details:
            name = detail.get('Name')
            if name == "reachability":
                return detail.get('Status')
        return None

