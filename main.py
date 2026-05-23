import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

converstation_history = []


user_question = "Can you check today's weather in Boston??"

fake_result = "Boston, MA: 72°F, partly cloudy, humidity 45%, wind 8 mph NW. High of 78°F, low of 62°F."

converstation_history.append(user_question)
converstation_history.append(fake_result)

system_prompt = """You are a research agent with access to these tools: web_search, calculator.

                When you need to use a tool, end your response with:
                [TOOL] tool_name [INPUT] your input here [END]

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

prompt = f"Question: {user_question}. {system_prompt}"

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

messages = [{"role": "user", "content": user_question}]

for i in range(5):
    message = client.messages.create(
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
        print(f"Final answer: {ai_response[final_start:final_end].strip()}")
        break

    elif "[TOOL]" in ai_response:
        messages.append({"role": "assistant", "content": ai_response})
        messages.append({"role": "user", "content": f"Tool result: {fake_result}"})

    else:
        messages.append({"role": "assistant", "content": ai_response})
        messages.append({"role": "user", "content": "Please respond with either [TOOL]...[END] or [FINAL]...[END] as instructed."})


    