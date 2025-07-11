import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

user_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    ),
)

if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    print(f"User prompt: {user_prompt}")
    print(
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
        + f"Response tokens: {response.usage_metadata.candidates_token_count}"
    )

if response.text != None:
    print(response.text)

if len(response.function_calls) > 0:
    for function_call in response.function_calls:
        if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
            results = call_function(function_call, True)
            print(f"-> {results.parts[0].function_response.response}")
        else:
            results = call_function(function_call)

        if results.parts[0].function_response.response == None:
            raise Exception("Fatal error ocurred")
