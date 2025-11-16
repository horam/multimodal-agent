import sys as system
import os
from dotenv import load_dotenv


# Load .env from the project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(ROOT_DIR, ".env")
load_dotenv(ENV_PATH)

from multimodal_agent.agent_core import MultiModalAgent
from multimodal_agent.utils import load_image_as_part

from .logger import get_logger
logger = get_logger(__name__)


def main():
    prompt_length = len(system.argv)
    if prompt_length < 2:
        usage()
        return

    command = system.argv[1]
    agent = MultiModalAgent()

    if command == "ask":
        if prompt_length < 3:
            logger.info('Error- correct usage:agent ask "your question"')
            return
        prompt = " ".join(system.argv[2:])
        response = agent.ask(prompt)
        logger.info(response)

    elif command == "image":
        if prompt_length < 4:
            logger.info('Error correct usage: agent image <img_path> "describe this"')
            return
        image = system.argv[2]
        image_as_part = load_image_as_part(image)
        prompt = " ".join(system.argv[3:])
        response = agent.ask_with_image(prompt, image_as_part)
        logger.info(response)
    elif command == "chat":
        agent.chat()
        return
    else:
        usage()


def usage():
    logger.info("This is a multi-modal agent that generates text based on an input image.")
    logger.info(
        """
        Usage:
            agent ask "your question"
            agent image <path/to/img> "your prompt"
            agent chat
        """
    )
