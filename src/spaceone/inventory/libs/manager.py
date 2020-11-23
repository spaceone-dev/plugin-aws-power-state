from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.connector import AWSConnector


class AWSPowerStateManager(BaseManager):
    connector_name = None
    response_schema = None

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """
        connector: AWSConnector = self.locator.get_connector('AWSConnector', secret_data=secret_data)
        connector.verify()

    def collect_power_state(self, params) -> list:
        raise NotImplemented

    def collect_resources(self, params) -> list:
        return self.collect_power_state(params)

