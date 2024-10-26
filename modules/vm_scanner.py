from os import environ
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient


'''
https://learn.microsoft.com/en-us/python/api/azure-mgmt-compute/azure.mgmt.compute.computemanagementclient?view=azure-python#azure-mgmt-compute-computemanagementclient-virtual-machines
'''

# Class VirtualMachineScanner


# Class VirtualMachine ScaleSet Scanner

class VirtualMachineScanner(ComputeManagementClient):
    def __init__(self, subscription_id:str = None):
        self.subscription_id = subscription_id

    def setup_compute_client(self) -> ComputeManagementClient:
        """Sets up the Authorization Management Client using DefaultAzureCredential."""
        try:
            cmc_client = ComputeManagementClient(
                DefaultAzureCredential(),
                self.subscription_id
            )
            return cmc_client
        except Exception as e:
            print(f"Failed to create AuthorizationManagementClient: {e}")
            return None


class VirtualMachineScaleSetScanner:
    pass



vm_client = VirtualMachineScanner(subscription_id=environ['AZURE_SUBSCRIPTION_ID'])