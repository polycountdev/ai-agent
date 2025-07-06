import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()

api_key = os.environ.get ("GEMINI_API_KEY")
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

    text = prompt
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
    resp_text = response.text


    if "--verbose" in args:
        print("Agent: " + resp_text + "\n" + "User prompt: " + prompt + "\n" + "Prompt tokens: " + str(response.usage_metadata.prompt_token_count) + "\n" + "Response tokens: " + str(response.usage_metadata.candidates_token_count))
    else:
        print(resp_text)
    

if __name__ == "__main__":
    main()
