#python script to check if a particular windows service is running, and start it if it is stopped,
# if status is unknown then stop the service and then start it.
# if it is disabled then enable it and start it

import win32serviceutil
import win32service
import winreg

def check_and_manage_service(service_name):
    try:
        # Check the status of the service
        status = win32serviceutil.QueryServiceStatus(service_name)[1]

        if status == win32service.SERVICE_RUNNING:
            print(f"The {service_name} service is already running.")
        elif status == win32service.SERVICE_STOPPED:
            print(f"The {service_name} service is stopped. Attempting to start it...")
            win32serviceutil.StartService(service_name)
            print(f"The {service_name} service has been started.")
        elif status in [win32service.SERVICE_START_PENDING, win32service.SERVICE_STOP_PENDING]:
            print(f"The {service_name} service status is pending. Please wait and try again.")
        else:
            print(f"The {service_name} service status is unknown. Attempting to restart it...")
            win32serviceutil.StopService(service_name)
            print(f"The {service_name} service has been stopped.")
            win32serviceutil.StartService(service_name)
            print(f"The {service_name} service has been restarted.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Attempting to enable the service and start it.")
        enable_and_start_service(service_name)

def enable_and_start_service(service_name):
    try:
        # Open the registry key for the service
        reg_path = f"SYSTEM\\CurrentControlSet\\Services\\{service_name}"
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_SET_VALUE)

        # Set the service start type to automatic (2)
        winreg.SetValueEx(reg_key, "Start", 0, winreg.REG_DWORD, 2)
        winreg.CloseKey(reg_key)

        print(f"The {service_name} service has been enabled.")
        win32serviceutil.StartService(service_name)
        print(f"The {service_name} service has been started.")
    except Exception as e:
        print(f"Failed to enable and start the {service_name} service: {e}")

if __name__ == "__main__":
    service_name = "Spooler"  # Replace with the name of your service
    check_and_manage_service(service_name)


#First, you'll need to install the pywin32 library if you haven't already.
# pip install pywin32