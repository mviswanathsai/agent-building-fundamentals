import os
import sys
from dotenv import load_dotenv
import ollama
from functions.config import available_tools
from config import system_prompt, model, max_iters
from call_function import call_function

def main():
    load_dotenv()
    v_flag = False

    if len(sys.argv) < 2:
        print("I need a prompt g")
        sys.exit(1)
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        v_flag = True

    prompt =  sys.argv[1]

    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
            ]

    out_token_count = 0
    for i in range(max_iters):
        response = ollama.chat(model=model, messages=messages, tools=available_tools)

        if response is None or response.eval_count is None:
            print("LLM response malformed")
        else:
            messages.append({"role":"model", "content": response.message.content})

        out_token_count += getattr(response, "eval_count", 0)

        if response.message.tool_calls:
            for tool in response.message.tool_calls:
                messages.append({"role":"model", "content": f"Calling {tool.function.name} with {tool.function.arguments}"})
                result = call_function(tool.function.name, tool.function.arguments, v_flag)
                messages.append({"role": "tool", "content": result})
        else:
            break

    out = response.message.content
    prompt_token_count = response.prompt_eval_count
    print(out)

    if v_flag:
        print(f"User Prompt: {prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {out_token_count}")


main()

