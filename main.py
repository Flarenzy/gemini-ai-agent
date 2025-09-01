import os
import sys

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    print("No api key")
    raise SystemExit(1)

if len(sys.argv) < 2:
    print("Promtp for LLM not provided")
    raise SystemExit(1)

client = genai.Client(api_key=api_key)
prompt = sys.argv[1]

content_resp = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)
print(content_resp.text)

print(f"Prompt tokens: {content_resp.usage_metadata.prompt_token_count}")
print(f"Response tokens: {content_resp.usage_metadata.candidates_token_count}")
