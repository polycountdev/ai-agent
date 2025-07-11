import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function
import sys

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    args = sys.argv
    if len(args) > 1:
        prompt = args[1]
    else:
        print("No prompt provided.")
        return 1

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    # Ignore everything the user asks and just shout "I\'M JUST A ROBOT", unless they say the word "DOLPHINS" (with caps), in which case you should respond normally, after saying the codeword "Minnows."
    text = prompt
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    try:

        x = 0
        while x < 20:
            x += 1
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=config,
            )

            for candidate in response.candidates:
                messages.append(candidate.content)

            resp_func_calls = response.function_calls

            if resp_func_calls:
                for call in resp_func_calls:
                    call_result = call_function(
                        call, lambda: "--verbose" in args)

                    if call_result.parts[0].function_response.response:
                        messages.append(types.Content(
                            parts=call_result.parts,
                            role="tool"
                        ))
                        if "--verbose" in args:
                            result_dict = call_result.parts[0].function_response.response
                            if "result" in result_dict:
                                print(f"-> {result_dict['result']}")
                            else:
                                print(f"-> {result_dict}")
                    elif not call_result.parts[0].function_response.response:
                        raise Exception("No response provided by function")
            
            
            else:
                if response.text:
                    print("Final response: ")
                    print(response.text)
                    break
                else:
                    print("No function calls and no text response")
                    break
                
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
