from azure.mgmt.monitor import MonitorManagementClient
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta
import os
import json


def get_activity_logs(resource_group, DEBUG=False, delta_days=7) -> dict:
    """
    Retrieves and optionally prints activity logs for a given Azure resource group.

    Args:
        resource_group (str): The name of the Azure resource group to retrieve activity logs for.
        DEBUG (bool, optional): If True, the function will print detailed logs to the console. 
                                Defaults to False.
        delta_days: Amount of days to search. Defaults to returning logs from the last 7 days.

    Returns:
        dict: A dictionary containing information about the log entry, including the caller,
              event message, operation name, timestamp, and caller's IP address. Returns None if no logs are found or an error occurs.

    Raises:
        Exception: If the MonitorManagementClient cannot be created or if there's an issue retrieving or processing activity logs.

    Notes:
        This function retrieves logs for the past 30 days from the specified resource group and 
        processes them. If DEBUG is set to True, it prints details about each log entry.
    """
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
        start_time = end_time - timedelta(days=30)
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
                    if DEBUG:
                        print(f"Operation: {log.operation_name.localized_value}")
                        print(f"Time: {time_stamp}")
                        print(f"Status: {log.status.localized_value}")
                        print(f"Resource: {log.resource_id}")
                        print(f"CallerIP: {ip_addr}")
                        print("-" * 40)
                    else:
                        return {
                            "caller": caller,
                            "event": event,
                            "operation_name": operation_name,
                            "time_stamp": time_stamp,
                            "caller_ip": ip_addr,
                        }

                except AttributeError as log_err:
                    print(f"Error processing log entry: {log_err}")
    except Exception as e:
        print(f"Error retrieving or processing activity logs: {e}")


def get_sign_in_logs():
    pass

