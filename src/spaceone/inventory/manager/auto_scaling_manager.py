import time
from spaceone.inventory.libs.manager import AWSPowerStateManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.auto_scaling import AutoScalingConnector
from spaceone.inventory.connector.ec2 import EC2Connector
from spaceone.inventory.model.auto_scaling import *


class AutoScalingManager(AWSPowerStateManager):
    connector_name = 'AutoScalingConnector'

    def collect_power_state(self, params):
        print("** Auto Scaling Start **")
        start_time = time.time()
        auto_scaling_conn: AutoScalingConnector = self.locator.get_connector(self.connector_name, **params)
        ec2_conn: EC2Connector = self.locator.get_connector('EC2Connector', **params)

        auto_scaling_resources = []

        for region_name in params.get('regions', []):
            # print(f'[ AutoScaling {region_name} ]')
            auto_scaling_conn.set_client(region_name)
            ec2_conn.set_client(region_name)

            for asg in auto_scaling_conn.describe_auto_scaling_groups():
                asg.update({
                    'instances': self.get_asg_instances(asg.get('Instances', []), ec2_conn),
                })

                auto_scaling_data = AutoScalingGroup(asg, strict=False)

                auto_scaling_resource = AutoScalingResource({
                    'data': auto_scaling_data,
                    'reference': ReferenceModel(auto_scaling_data.reference())
                })

                auto_scaling_resources.append(AutoScalingResponse({'resource': auto_scaling_resource}))

        print(f' Auto Scaling Finished {time.time() - start_time} Seconds')
        return auto_scaling_resources

    def get_asg_instances(self, instances, ec2_conn):
        max_count = 20
        instances_from_ec2 = []
        split_instances = [instances[i:i + max_count] for i in range(0, len(instances), max_count)]

        for instances in split_instances:
            instance_ids = [_instance.get('InstanceId') for _instance in instances if _instance.get('InstanceId')]
            instances_from_ec2.extend(ec2_conn.describe_instances(is_paginate=False, InstanceIds=instance_ids))

        for instance in instances:
            for instance_from_ec2 in instances_from_ec2:
                if instance_from_ec2.get('InstanceId') == instance.get('InstanceId'):
                    instance.update({
                        'lifecycle': instance_from_ec2.get('InstanceLifecycle', 'scheduled')
                    })
                    break

        return instances