# jenkins/jenkins_main.py

import requests
import re
import json
from pathlib import Path
from memory.projects import register_project
from memory.env import update_installed_packages

register_project("clip_syncer", "/home/dev/projects/clip_syncer", "Tool to sync audio clips across formats")
update_installed_packages(["requests", "numpy", "openai"])

LLM_URL = "http://localhost:11434/generate"
INJECTED_PROMPT_PATH = Path("jenkins/injected_prompt.txt")
DRISCOLL_EXECUTE_URL = "http://192.168.1.100:8000/execute"

def load_injected_prompt():
    return INJECTED_PROMPT_PATH.read_text()

def build_prompt(user_input: str) -> str:
    injected = load_injected_prompt()
    return f"{injected}\n\nUSER:\n{user_input.strip()}\n\nJenkins:"

def send_to_llm(prompt: str) -> str:
    response = requests.post(LLM_URL, json={
        "prompt": prompt,
        "stream": False,
    })
    response.raise_for_status()
    return response.json()["response"]

def extract_exec_blocks(text: str) -> list[str]:
    return re.findall(r"EXECUTE:\n(.+?)(?=(\n\n|\Z))", text, flags=re.DOTALL)

def send_command_to_driscoll(command: str) -> str:
    response = requests.post(DRISCOLL_EXECUTE_URL, json={"command": command})
    response.raise_for_status()
    return response.json()["output"]

def main():
    user_input = input("Task: ")
    prompt = build_prompt(user_input)
    print("\n>>> Sending to DeepSeek...\n")
    response = send_to_llm(prompt)
    print(">>> LLM Response:\n")
    print(response)

    exec_blocks = extract_exec_blocks(response)
    for cmd, _ in exec_blocks:
        print("\n>>> Executing Command on Driscoll:\n", cmd.strip())
        output = send_command_to_driscoll(cmd.strip())
        print("\n>>> Output:\n", output)

if __name__ == "__main__":
    main()
