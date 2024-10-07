from azure.mgmt.monitor import MonitorManagementClient
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta
import os
import json


def return_activity_logs(resource_group):
    try:
        mmc_client = MonitorManagementClient(
                                    DefaultAzureCredential(), 
                                    os.environ['AZURE_SUBSCRIPTION_ID']
                                    )
    except Exception as e:
        print(f"Failed to create MonitorManagementClient: {e}")
        return

    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=2)
        filter = f"eventTimestamp ge '{start_time}' and eventTimestamp le '{end_time}' and resourceGroupName eq '{resource_group}'"
        
        activity_logs = mmc_client.activity_logs.list(filter=filter)
        if not activity_logs:
            print("No activity logs found")
        else:
            for log in activity_logs:
                try:
                    caller = log.caller
                    event = log.properties.get('message', 'None')
                    operation_name = log.operation_name.localized_value
                    time_stamp = log.event_timestamp
                    ip_addr = log.claims.get('ipaddr', 'None')
                    print(f"Operation: {log.operation_name.localized_value}")
                    print(f"Time: {time_stamp}")
                    print(f"Status: {log.status.localized_value}")
                    print(f"Resource: {log.resource_id}")
                    print(f"CallerIP: {ip_addr}")
                    print("-" * 40)

                except AttributeError as log_err:
                    print(f"Error processing log entry: {log_err}")
    except Exception as e:
        print(f"Error retrieving or processing activity logs: {e}")

return_activity_logs("")