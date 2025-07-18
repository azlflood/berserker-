# jenkins/api.py

from fastapi import FastAPI
from pydantic import BaseModel
from memory.env import save_env
import uvicorn

app = FastAPI()

class EnvInfo(BaseModel):
    machine_name: str
    ip: str
    os: str
    python_version: str
    installed_packages: list[str]
    last_updated: str

@app.post("/api/update-env")
def update_env(data: EnvInfo):
    save_env(data.dict())
    return {"status": "ok", "message": "Environment updated."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
