import sys as system
import os
from dotenv import load_dotenv


# Load .env from the project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(ROOT_DIR, ".env")
load_dotenv(ENV_PATH)

from multimodal_agent.agent_core import MultiModalAgent
from multimodal_agent.utils import load_image_as_part


def main():
    prompt_length = len(system.argv)
    if prompt_length < 2:
        usage()
        return

    command = system.argv[1]
    agent = MultiModalAgent()

    if command == "ask":
        if prompt_length < 3:
            print('Error- correct usage:agent ask "your question"')
            return
        prompt = system.argv[2]
        response = agent.ask(prompt)
        print(response)

    elif command == "image":
        if prompt_length < 4:
            print('Error correct usage: agent image <img_path> "describe this"')
            return
        image = system.argv[2]
        image_as_part = load_image_as_part(image)
        prompt = system.argv[3]
        response = agent.ask_with_image(prompt, image_as_part)
        print(response)
    elif command == "chat":
        agent.chat()
        return
    else:
        usage()


def usage():
    print("This is a multi-modal agent that generates text based on an input image.")
    print(
        """
        Usage:
            agent ask "your question"
            agent image <path/to/img> "your prompt"
            agent chat
        """
    )
