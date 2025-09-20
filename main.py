import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.
You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not
need to specify the working directory in your function calls as it is
automatically injected for security reasons.
"""


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

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=("Lists files in the specified directory along with "
                 "their sizes, constrained to the working directory."),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=("The directory to list files from, relative to "
                             "the working directory. If not provided, lists "
                             "files in the working directory itself."),
            ),
        },
        required=[]
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
model_config = types.GenerateContentConfig(tools=[available_functions],
                                           system_instruction=system_prompt)
content_resp = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents=messages,
                                              config=model_config
                                              )


if content_resp.function_calls:
    for function_call_part in content_resp.function_calls:
        print(f"Calling function: {function_call_part.name}"
              f"({function_call_part.args})")

if content_resp.text is not None:
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
