import config 
import modules.activity_logs as activity_logs_client






logs = activity_logs_client.get_activity_logs("python-project-test-resources", DEBUG=True)
# print(logs)