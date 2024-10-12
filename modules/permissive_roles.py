from os import environ
from operator import itemgetter
from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient

'''
https://learn.microsoft.com/en-us/python/api/azure-mgmt-authorization/azure.mgmt.authorization.v2022_04_01.authorizationmanagementclient?view=azure-python
'''

def list_roles(subscription_id):
    amc: AuthorizationManagementClient = setup_auth_client()
        
    roles = amc.role_assignments.list_for_subscription(filter='atScope()')
    for role in roles:
        id = role.id
        scope = role.scope
        created_on  = role.created_on
        updated_on = role.updated_on
        principal_id = role.principal_id

        print(f"id: {id}")
        print(f"Scope: {scope}")
        print(f"principal_id: {principal_id}")
        print(f"Created_time: {created_on}")
        print(f"Updated_time: {updated_on}")
        print("-" * 40)

    try:
        pass

    except Exception as e:
        print("Error occurred {e}")


def search_for_dangerous_roles(roles_object):
    pass


def setup_auth_client():
    try:
        amc_client: AuthorizationManagementClient = AuthorizationManagementClient(
                                    DefaultAzureCredential(), 
                                    environ['AZURE_SUBSCRIPTION_ID']
                                    )
        return amc_client
    
    except Exception as e:
        print(f"Failed to create MonitorManagementClient: {e}")
        return
    

list_roles(environ['AZURE_SUBSCRIPTION_ID'])