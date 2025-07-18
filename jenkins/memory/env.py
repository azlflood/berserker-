# jenkins/memory/env.py

import json
from pathlib import Path
from datetime import datetime

ENV_PATH = Path("jenkins/memory/env_info.json")

def load_env():
    if ENV_PATH.exists():
        return json.loads(ENV_PATH.read_text())
    return {}

def save_env(env_data: dict):
    env_data["last_updated"] = datetime.utcnow().isoformat()
    ENV_PATH.write_text(json.dumps(env_data, indent=2))

def update_installed_packages(new_list: list[str]):
    env = load_env()
    env["installed_packages"] = sorted(set(new_list))
    save_env(env)
