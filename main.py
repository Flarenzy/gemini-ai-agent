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
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of a file specified by the file path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=("The file path to the file from which to"
                             "read the contents of"),
            ),
        },
        required=["file_path"]
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file specified by the file_path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file"
            )
        },
        required=["file_path", "content"]
    )
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=("Run a python file specified by a file path with "
                 "optional args (list[str])"),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the python file to run."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description=("List of strings containging args to pass to the"
                             " python file that will be run"),
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Arg to pass"
                )
            )
        },
        required=["file_path"]
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
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
