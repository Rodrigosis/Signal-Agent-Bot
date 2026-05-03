import os
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
import requests

load_dotenv()
OWNER = os.getenv("GITHUB_OWNER")
REPO = os.getenv("GITHUB_REPO")
FILE_PATH = os.getenv("GITHUB_FILE_PATH")
BRANCH = os.getenv("GITHUB_BRANCH")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

response = requests.get(
    url=f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}",
    headers={"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github.raw"},
    params = {"ref": BRANCH}
)

if response.status_code != 200:
    raise SystemExit(f"Error getting prompt from GitHub: {response.status_code} -- {response.text}")

SYSTEM_PROMPT = SystemMessage(content=response.content)
