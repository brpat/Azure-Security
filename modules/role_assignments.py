from os import environ
from operator import itemgetter
from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient

'''
https://learn.microsoft.com/en-us/python/api/azure-mgmt-authorization/azure.mgmt.authorization.v2022_04_01.authorizationmanagementclient?view=azure-python
https://learn.microsoft.com/en-us/rest/api/authorization/role-definitions/get?view=rest-authorization-2022-04-01&tabs=Python&tryIt=true&source=docs#code-try-0
'''

class AzureRoleAuditor:
    def __init__(self, subscription_id: str):
        self.subscription_id = subscription_id
        self.amc_client = self.setup_auth_client()
    
    def setup_auth_client(self) -> AuthorizationManagementClient:
        """Sets up the Authorization Management Client using DefaultAzureCredential."""
        try:
            amc_client = AuthorizationManagementClient(
                DefaultAzureCredential(),
                self.subscription_id
            )
            return amc_client
        except Exception as e:
            print(f"Failed to create AuthorizationManagementClient: {e}")
            return None

    def list_role_assignments(self):
        """Lists role assignments for the given subscription."""
        if not self.amc_client:
            print("AuthorizationManagementClient is not initialized.")
            return
        
        try:
            roles = self.amc_client.role_assignments.list_for_subscription(filter='atScope()')
            for role in roles:
                assignment_id = role.id
                scope = role.scope
                role_name = self.role_id_to_name(role.role_definition_id.split("/")[-1])
                created_on = role.created_on
                updated_on = role.updated_on
                principal_id = role.principal_id

                print(f"id: {assignment_id}")
                print(f"RoleName: {role_name}")
                print(f"Scope: {scope}")
                print(f"principal_id: {principal_id}")
                print(f"Created_time: {created_on}")
                print(f"Updated_time: {updated_on}")
                print("-" * 40)
        except Exception as e:
            print(f"Error occurred: {e}")
    
    def role_id_to_name(self, role_definition_id: str) -> str:
        """Converts role_definition_id to role name."""

        if not self.amc_client:
            print("AuthorizationManagementClient is not initialized.")
            return

        role_object = self.amc_client.role_definitions.get(scope=f"/subscriptions/{self.subscription_id}", role_definition_id=role_definition_id )
        return role_object.role_name


    def search_for_dangerous_roles(self):
        """Searches for potentially dangerous roles. This needs to be implemented."""
        pass
    
# Usage
auditor = AzureRoleAuditor(subscription_id=environ['AZURE_SUBSCRIPTION_ID'])
auditor.list_role_assignments()
print(auditor.role_id_to_name("acdd72a7-3385-48ef-bd42-f606fba81ae7"))
# list_role_assignments(environ['AZURE_SUBSCRIPTION_ID'])