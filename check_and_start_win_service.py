import win32serviceutil

def check_and_start_service(service_name):
    try:
        # Check the status of the service
        status = win32serviceutil.QueryServiceStatus(service_name)[1]

        if status == 4:  # 4 means the service is running
            print(f"The {service_name} service is already running.")
        else:
            print(f"The {service_name} service is not running. Attempting to start it...")
            win32serviceutil.StartService(service_name)
            print(f"The {service_name} service has been started.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    service_name = "WSLService"  # Replace with the name of your service
    check_and_start_service(service_name)
