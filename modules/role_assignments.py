from os import environ
from operator import itemgetter
from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.authorization.v2022_04_01.models import Permission

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
                is_custom_role: dict = self.check_for_custom_privileged_role(role.role_definition_id)
                assignment_id = role.id
                scope = role.scope
                role_name = self.role_id_to_name(role.role_definition_id.split("/")[-1])
                created_on = role.created_on
                updated_on = role.updated_on
                principal_id = role.principal_id                
                is_permissive = "PERMISSIVE_ROLE!" if (AzureRoleAuditor.search_for_builtin_privileged_roles(role_name) 
                                                       or is_custom_role.get("permissive")) else "STANDARD_ROLE"

                print(f"id: {assignment_id}")
                print(f"RoleName: {role_name}")
                print(f"Scope: {scope}")
                print(f"TYPE: {is_permissive}")
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
    
    def check_for_custom_privileged_role(self, role_definition_id: str) -> bool:
        if not self.amc_client:
            print("AuthorizationManagementClient is not initialized.")
            return

        try:
            overly_permissive_perms: list = list()
            role_name = self.role_id_to_name(role_definition_id.split("/")[-1])
            role_definition = self.amc_client.role_definitions.get_by_id(role_definition_id)
            # print(role_definition)
            if role_definition.role_type != 'BuiltInRole':
                for permission in role_definition.permissions:
                    overly_permissive_perms = self.__check_priviledged_permission(permission)

                if overly_permissive_perms:
                    print(f"Dangerous permissions detected in custom role {role_name}")
                    print(f"Allow: {overly_permissive_perms}")
                    return {
                        "type": 'Custom',
                        "permissive": True,
                        "excessive_permissions": overly_permissive_perms
                        }
                else:
                    return {
                        "type": 'Custom',
                        "permissive": False,
                        "excessive_permissions": overly_permissive_perms
                        }
            else:
                return {"type": 'BuiltInRole'}
        except Exception as e:
            print(f"Error occurred: {e}")

    def __check_priviledged_permission(self, permissions_object: Permission) -> list:
        permissive_perms = list()
        
        permissive_perms_lst = [
            "*",
            "Microsoft.Compute/*",
            "Microsoft.Storage/*",
            "Microsoft.Network/*",
            "Microsoft.KeyVault/*",
            "Microsoft.Resources/*",
            "Microsoft.ContainerService/*",
            "Microsoft.Sql/*",
            "Microsoft.Security/*",
            "Microsoft.Authorization/*",
            "Microsoft.Automation/*"
        ]

        for allowed_action in permissions_object.actions:
            if allowed_action in permissive_perms_lst:
                permissive_perms.append(allowed_action)
        if permissive_perms:
            return permissive_perms

    @staticmethod
    def search_for_builtin_privileged_roles(role_name: str) -> bool:
        """Compares input Azure RBAC role to list of permissive built roles. 
        Returns true if role matches one of permissive roles."""
        
        azure_permissive_roles: list[str] = [
                        "Owner",
                        "User Access Administrator",
                        "Contributor",
                        "Role Based Access Control Administrator",
                        "User Access Administrator"
                    ]

        return role_name in azure_permissive_roles

# Usage
auditor = AzureRoleAuditor(subscription_id=environ['AZURE_SUBSCRIPTION_ID'])
auditor.list_role_assignments()
# print(auditor.role_id_to_name("acdd72a7-3385-48ef-bd42-f606fba81ae7"))
# list_role_assignments(environ['AZURE_SUBSCRIPTION_ID'])