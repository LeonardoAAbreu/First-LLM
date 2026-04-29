import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_functions import available_functions, call_function
from prompts import system_prompt


def main():
    # print("Hello from boot-dev-bot!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    parser = argparse.ArgumentParser(description="Ask ai whatever: ")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        done = content_generator(api_key, messages, args)
        if done:
            break
    else:
        print("AI ran too much, got exausted")
        sys.exit(1)


def content_generator(api_key, messages, args):
    function_result = []

    if api_key is None:
        raise RuntimeError("no api key")
    else:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )
        response_usage = response.usage_metadata

        for r in response.candidates:
            messages.append(r.content)

        if (
            response_usage.prompt_token_count
            == response_usage.candidates_token_count
            == None
        ):
            raise RuntimeError("error in token usage")
        else:
            if args.verbose:
                print(f"User prompt: {str(args.user_prompt)}")
                print(f"Prompt tokens: {response_usage.prompt_token_count}")
                print(f"Response tokens: {response_usage.candidates_token_count}")

            if response.function_calls:
                for f in response.function_calls:
                    # print(f"Calling function: {f.name}({f.args})")
                    function_call_result = call_function(f, args.verbose)
                    if not function_call_result.parts:
                        raise Exception(
                            "Result of the function is null, or function doesn't exist"
                        )
                    elif not function_call_result.parts[0].function_response:
                        raise Exception("No response associated with function")
                    elif not function_call_result.parts[0].function_response.response:
                        raise Exception("No result from function")
                    else:
                        function_result.append(function_call_result.parts[0])
                        if args.verbose:
                            print(
                                f"-> {function_call_result.parts[0].function_response.response}"
                            )
            else:
                print(response.text)
                return True

        messages.append(types.Content(role="user", parts=function_result))


if __name__ == "__main__":
    main()
