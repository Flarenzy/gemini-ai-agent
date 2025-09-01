import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

parser = argparse.ArgumentParser()
parser.add_argument("--verbose",
                    action="store_true",
                    help="Print verbose output if flag is present")
# positional arg
parser.add_argument("prompt",
                    action="store",
                    type=str,
                    default="",
                    help="Prompt to pass to the Gemini LLM")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    print("No api key")
    raise SystemExit(1)
if args.prompt == "":
    print("No prompt provided")
    raise SystemExit(1)

client = genai.Client(api_key=api_key)
user_prompt = args.prompt

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
content_resp = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents=user_prompt)

if content_resp.text is None:
    print("Error getting resp text")
    raise SystemExit(1)

print(content_resp.text)

if args.verbose:
    print(f"User prompt: {user_prompt}")
    if content_resp.usage_metadata is None:
        print("Error getting usage data")
    else:
        prompt_tokens = (f"Prompt tokens: "
                         f"{content_resp.usage_metadata.prompt_token_count}")
        resp_tokens = (f"Response tokens: "
                       f"{content_resp.usage_metadata.candidates_token_count}")
        print(prompt_tokens)
        print(resp_tokens)
