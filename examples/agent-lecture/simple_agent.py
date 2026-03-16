import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath("../../"))
from langchain.agents import create_agent

from util.models import get_model
from util.streaming_utils import STREAM_MODES, handle_stream
from util.pretty_print import get_user_input
from util.tools import get_web_search_tool

def run():
    # Get predefined attributes
    model = get_model(top_p = 0.9, temprature = 0.03)

    # Create agent
    agent = create_agent(
        model=model,
        tools=[get_web_search_tool],
        system_prompt=(
            "Du är en hjälpsam assistent som svarar på användarens frågor."
            "Svara alltid på svenska och var koncis men informativ."
        ),
    )

    messages =[]

    while True:
        user_input = get_user_input("Ställ din fråga")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Avslutar...")
            break
        if not user_input.strip():
            continue
        messages.append({"role": "user", "content": user_input })
    # Call the agent
        process_stream = agent.stream(
            {"messages": messages},
            stream_mode=STREAM_MODES,
    )

    # Stream the process
        response = handle_stream(process_stream)

        messages.append({"role": "user", "content": response })
       

if __name__ == "__main__":
    run()
