import os
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
import requests

load_dotenv()

# response = requests.get(
#     url=f'https://raw.githubusercontent.com/{os.getenv("GITHUB_PROMPT_FILE")}',
#     headers={"Authorization": os.getenv("GITHUB_TOKEN")}
# )
#
# if response.status_code != 200:
#     raise SystemExit(f"Error getting prompt from GitHub: {response.status_code}")
#
# SYSTEM_PROMPT = SystemMessage(
#     content=f"""
# {response.content}
# """
# )

SYSTEM_PROMPT = SystemMessage(
    content=f"""

"""
)

if __name__ == "__main__":
    print(SYSTEM_PROMPT)
