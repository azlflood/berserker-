# jenkins/memory/projects.py

import json
from pathlib import Path
from datetime import datetime

PROJECTS_PATH = Path("jenkins/memory/projects.json")

def load_projects():
    if PROJECTS_PATH.exists():
        return json.loads(PROJECTS_PATH.read_text())
    return {"projects": []}

def save_projects(data: dict):
    PROJECTS_PATH.write_text(json.dumps(data, indent=2))

def register_project(name: str, path: str, description: str = "", status: str = "active"):
    data = load_projects()
    now = datetime.utcnow().isoformat()
    project = {
        "name": name,
        "path": path,
        "description": description,
        "status": status,
        "created_at": now,
        "last_modified": now
    }
    data["projects"].append(project)
    save_projects(data)

def update_project(name: str, **updates):
    data = load_projects()
    for project in data["projects"]:
        if project["name"] == name:
            project.update(updates)
            project["last_modified"] = datetime.utcnow().isoformat()
            break
    save_projects(data)
