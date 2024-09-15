from azure.mgmt.monitor import MonitorManagementClient
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta
import os
import json


def return_activity_logs(resource_group):
    mmc_client = MonitorManagementClient(
                                DefaultAzureCredential(), 
                                os.environ['AZURE_SUBSCRIPTION_ID']
                                )

    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)
    filter=f"eventTimestamp ge '{start_time}' and eventTimestamp le '{end_time}' and resourceGroupName eq '{resource_group}'"
    # print(filter)
    activity_logs = mmc_client.activity_logs.list(filter=filter)
    
    for log in activity_logs:
        json.loads(str(log))
        caller = log.get("caller", "None")
        event = log.get("message", "None")
        operation_name = log.get("operation_name", "None")
        time_stamp = log.get("event_timestamp", "None")
        ip_addr = log.get("ipaddr", "None")
        print(caller, event, operation_name, time_stamp, ip_addr)
        exit()
    
return_activity_logs(MYRESOURCEGROUP)