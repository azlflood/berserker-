# driscoll/driscoll_executor.py

from fastapi import FastAPI
from pydantic import BaseModel
from subprocess import run, PIPE
import uvicorn
import shlex
import re

app = FastAPI()

SAFE_DIR = "/home/jenkinsbot"  # Adjust if needed
ALLOWED_COMMANDS = [
    "python", "pip", "ls", "cat", "cd", "mkdir", "touch", "echo", "pytest", "tree"
]
DENY_PATTERNS = [
    r"rm\s+-rf\s+/", r"sudo", r"reboot", r"shutdown", r"curl\s+.+\|", r"wget\s+.+\|", r"dd\s+if="
]

class CommandRequest(BaseModel):
    command: str

def is_safe(command: str) -> bool:
    # Must begin with something allowed
    if not any(command.strip().startswith(cmd) for cmd in ALLOWED_COMMANDS):
        return False
    # Must not match any deny patterns
    for pattern in DENY_PATTERNS:
        if re.search(pattern, command):
            return False
    return True

@app.post("/execute")
async def execute_command(data: CommandRequest):
    command = data.command.strip()

    if not is_safe(command):
        return {"success": False, "output": f"❌ Rejected unsafe command:\n{command}"}

    # Wrap in safe shell context
    full_command = f"cd {shlex.quote(SAFE_DIR)} && {command}"

    try:
        result = run(full_command, shell=True, capture_output=True, text=True, timeout=60)
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        return {"success": True, "output": output.strip()}
    except Exception as e:
        return {"success": False, "output": f"⚠️ Execution error: {e}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
