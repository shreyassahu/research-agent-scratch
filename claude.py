import os
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
from calculator import calculate_expression
from web_search import get_web_result
from datetime import date

load_dotenv()


async def call_claude(user_question):
    tools_used = []

    system_prompt = f"""You are a research agent with access to these tools: web_search, calculator.

                    Today's date is {date.today()}

                    When you need to use a tool, end your response with:
                    [TOOL] tool_name [INPUT] your input here [END]

                    After receiving tool results, first assess: Is this information sufficient, reliable, and relevant? 
                    If not, explain what's missing and try a different approach.

                    When you have enough information to give a final answer, end your response with:
                    [FINAL] your complete answer here [END]

                    You must ALWAYS end with either [TOOL]...[END] or [FINAL]...[END]. No exceptions.

                    Examples:

                    User: What's the weather in Boston today?
                    Assistant: I need to search for current weather data.
                    [TOOL] web_search [INPUT] weather in Boston today [END]

                    User: What is 15% of 340?
                    Assistant: Let me calculate that.
                    [TOOL] calculator [INPUT] 340 * 0.15 [END]

                    User: Who wrote Hamlet?
                    Assistant: I already know this from my training data.
                    [FINAL] William Shakespeare wrote Hamlet, believed to have been written between 1599 and 1601. [END]"""


    client = AsyncAnthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    messages = [{"role": "user", "content": user_question}]

    for i in range(6):

        try:
            message = await client.messages.create(
                max_tokens=1024,
                system=system_prompt,
                messages=messages,
                model="claude-sonnet-4-5",
            )

            ai_response = message.content[0].text

            print(f"\n--- Iteration {i+1} ---")
            print(f"Claude: {ai_response}")

            if "[FINAL]" in ai_response:
                final_start = ai_response.find("[FINAL]") + 7
                final_end = ai_response.find("[END]")
                final_answer = ai_response[final_start:final_end].strip()
                print(f"Final answer: {final_answer}")
                return {"answer" : final_answer, "iterations": i+1, "tools_used": tools_used}
                

            elif "[TOOL]" in ai_response:
                messages.append({"role": "assistant", "content": ai_response})

                input_start = ai_response.find("[INPUT]") + 7
                input_end = ai_response.find("[END]")
                tool_start = ai_response.find("[TOOL]") + 6
                tool_end = ai_response.find("[INPUT]")

                tool_input = ai_response[input_start:input_end].strip()
                tool_name = ai_response[tool_start:tool_end].strip()

                tools_used.append(tool_name)

                tool_result = ""

                if tool_name == "web_search":
                    tool_result = await get_web_result(tool_input)
                elif tool_name == "calculator":
                    tool_result = calculate_expression(tool_input)

                messages.append({"role": "user", "content": f"Tool result: {tool_result}"})

            else:
                if i == 4:
                    messages.append({"role": "assistant", "content": ai_response})
                    messages.append({"role": "user", "content": "You've used all your tool calls. Give your [FINAL] answer with what you have."})
                else:
                    messages.append({"role": "assistant", "content": ai_response})
                    messages.append({"role": "user", "content": "Please respond with either [TOOL]...[END] or [FINAL]...[END] as instructed."})


        except Exception as e:
            return {"msg" : "Unable to fetch response from Claude"}    