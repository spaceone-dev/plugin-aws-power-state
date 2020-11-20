import time
import logging
import concurrent.futures

from spaceone.core.service import *
from spaceone.inventory.libs.connector import AWSConnector


_LOGGER = logging.getLogger(__name__)
MAX_WORKER = 20
SUPPORTED_RESOURCE_TYPE = ['inventory.Server', 'inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
DEFAULT_REGION = 'us-east-1'
FILTER_FORMAT = []


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

        self.execute_managers = [
            'EC2Manager',
            'AutoScalingManager',
            'RDSManager'
        ]

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE
        }
        return {'metadata': capability}

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})

        if secret_data != {}:
            self.get_account_id(secret_data)

        return {}

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def list_resources(self, params):
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
        """

        secret_data = params['secret_data']

        params.update({
            'account_id': self.get_account_id(secret_data),
            'regions': self.get_regions(secret_data)
        })

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            print("[ EXECUTOR START ]")
            future_executors = []
            for execute_manager in self.execute_managers:
                print(f'@@@ {execute_manager} @@@')
                _manager = self.locator.get_manager(execute_manager)
                future_executors.append(executor.submit(_manager.collect_resources, params))

            for future in concurrent.futures.as_completed(future_executors):
                for resource in future.result():
                    yield resource.to_primitive()

        print(f'TOTAL TIME : {time.time() - start_time} Seconds')

    @staticmethod
    def get_account_id(secret_data, region=DEFAULT_REGION):
        aws_connector = AWSConnector(secret_data=secret_data)
        aws_connector.service = 'sts'
        aws_connector.set_client(region)
        return aws_connector.client.get_caller_identity()['Account']

    @staticmethod
    def get_regions(secret_data):
        if 'region_name' in secret_data:
            return [secret_data.get('region_name')]
        else:
            aws_connector = AWSConnector(secret_data=secret_data)
            aws_connector.service = 'ec2'
            aws_connector.set_client(DEFAULT_REGION)
            return list(map(lambda region_info: region_info.get('RegionName'),
                            aws_connector.client.describe_regions().get('Regions')))
