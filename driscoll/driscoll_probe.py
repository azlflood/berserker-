# driscoll/driscoll_probe.py

import platform
import subprocess
import json
import requests
from datetime import datetime

# Set this to Jenkins' endpoint for receiving env updates
JENKINS_ENV_URL = "http://192.168.1.200:5000/api/update-env"  # Starblazer IP or hostname

def get_os_info():
    return platform.platform()

def get_python_version():
    return platform.python_version()

def get_installed_packages():
    try:
        output = subprocess.check_output(["pip", "list", "--format", "json"], text=True)
        packages = json.loads(output)
        return [pkg["name"] for pkg in packages]
    except Exception as e:
        return [f"<error: {e}>"]

def build_payload():
    return {
        "machine_name": platform.node(),
        "ip": "192.168.1.100",  # or use socket.gethostbyname(socket.gethostname())
