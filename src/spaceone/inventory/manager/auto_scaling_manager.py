import time
from spaceone.inventory.libs.manager import AWSPowerStateManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.auto_scaling import AutoScalingConnector
from spaceone.inventory.model.auto_scaling import *


class AutoScalingManager(AWSPowerStateManager):
    connector_name = 'AutoScalingConnector'

    def collect_power_state(self, params):
        print("** Auto Scaling Start **")
        start_time = time.time()
        auto_scaling_conn: AutoScalingConnector = self.locator.get_connector(self.connector_name, **params)

        auto_scaling_resources = []

        for region_name in params.get('regions', []):
            # print(f'[ AutoScaling {region_name} ]')
            auto_scaling_conn.set_client(region_name)

            for asg in auto_scaling_conn.describe_auto_scaling_groups():
                auto_scaling_data = AutoScalingGroup(asg, strict=False)

                auto_scaling_resource = AutoScalingResource({
                    'data': auto_scaling_data,
                    'reference': ReferenceModel(auto_scaling_data.reference())
                })

                auto_scaling_resources.append(AutoScalingResponse({'resource': auto_scaling_resource}))

        print(f' Auto Scaling Finished {time.time() - start_time} Seconds')
        return auto_scaling_resources
