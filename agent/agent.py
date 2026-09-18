import json
from agent.llm import ask_llm, LLMServiceError
from tools.tool_registry import TOOLS
from agent.memory import add_message, get_history


def run_agent(message, max_iterations=3):
    add_message("user", message)

    prompt = f"""
You are an AI agent.

You have access to these tools:

calculator:
{TOOLS["calculator"]["description"]}

house_price_predictor:
{TOOLS["house_price_predictor"]["description"]}

Decide what action should be taken for the user's message.

If the user asks for a mathematical calculation, choose calculator.

If the user asks to predict a house price and provides all 8 required numerical features, choose house_price_predictor.

If the user asks for a house price prediction but does not provide all 8 required features, choose respond and ask the user to provide the missing features.

Never invent or guess feature values.
Never use example values as actual user input.

Otherwise, choose respond.

Return ONLY valid JSON in exactly one of these formats:

{{"action": "calculator", "input": "25 * 48"}}

or

{{"action": "house_price_predictor", "input": [8.3, 25, 5.0, 1.0, 300, 2.5, 37.0, -122.0]}}

or

{{"action": "respond", "input": "your answer to the user"}}

Conversation history:
{get_history()}

Current user message:
{message}
"""

    for iteration in range(max_iterations):

        # Ask Gemini to decide the next action
        try:
            response = ask_llm(prompt)

        except LLMServiceError as error:
            return {
                "action": "error",
                "answer": str(error)
            }

        # Convert Gemini's JSON response into Python
        try:
            decision = json.loads(response)

        except json.JSONDecodeError:
            return {
                "action": "error",
                "answer": "I couldn't process the agent's decision. Please try again."
            }

        # Validate the agent decision
        if "action" not in decision or "input" not in decision:
            return {
                "action": "error",
                "answer": "The agent returned an invalid decision. Please try again."
            }

        # -------------------------
        # DIRECT RESPONSE
        # -------------------------

        if decision["action"] == "respond":

            answer = decision["input"]

            add_message("assistant", answer)

            return {
                "action": "respond",
                "answer": answer
            }

        # -------------------------
        # CALCULATOR TOOL
        # -------------------------

        if decision["action"] == "calculator":

            tool = TOOLS["calculator"]

            try:
                result = tool["function"](decision["input"])

            except ValueError as error:
                return {
                    "action": "calculator",
                    "error": str(error)
                }

            add_message(
                "tool",
                f"Calculator result: {result}"
            )

            prompt = f"""
The calculator tool returned:

{result}

Conversation history:
{get_history()}

Now decide what to do next.

If the user's request is complete, choose respond.

If another tool is required, choose that tool.

Return ONLY valid JSON.

Final answer:
{{"action": "respond", "input": "your final answer"}}

Calculator:
{{"action": "calculator", "input": "mathematical expression"}}

House price prediction:
{{"action": "house_price_predictor", "input": [8 numerical features]}}
"""

            continue

        # -------------------------
        # HOUSE PRICE MODEL
        # -------------------------

        if decision["action"] == "house_price_predictor":

            tool = TOOLS["house_price_predictor"]

            try:
                result = tool["function"](decision["input"])

            except ValueError as error:
                return {
                    "action": "house_price_predictor",
                    "error": str(error)
                }

            add_message(
                "tool",
                f"House price prediction: {result}"
            )

            prompt = f"""
The house price prediction model returned:

{result}

The prediction is measured in units of $100,000.

Conversation history:
{get_history()}

Now decide what to do next.

If the user's request is complete, choose respond.

If another tool is required, choose that tool.

Return ONLY valid JSON.

Final answer:
{{"action": "respond", "input": "your final answer"}}

Calculator:
{{"action": "calculator", "input": "mathematical expression"}}

House price prediction:
{{"action": "house_price_predictor", "input": [8 numerical features]}}
"""

            continue

    return {
            "action": "error",
            "answer": f"Unknown agent action: {decision['action']}"
    }