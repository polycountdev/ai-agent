import os
from pathlib import Path
from google.genai import types
import functions as funcs
from functions import *
from functions import function_map


def call_function(function_call_part, verbose=False):
    func_name = function_call_part.name
    func_args = function_call_part.args
    func_args["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {func_name}({func_args})")
    else:
        print(f"Calling function: {func_name}")

    if func_name not in function_map.func_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )

    func_to_call = function_map.func_dict[func_name]
    result = func_to_call(**func_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": result},
            )
        ],
    )
