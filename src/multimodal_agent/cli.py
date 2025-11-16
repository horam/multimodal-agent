import argparse
import sys as system
import os

from dotenv import load_dotenv

from multimodal_agent.agent_core import MultiModalAgent
from multimodal_agent.utils import load_image_as_part
from .errors import AgentError, InvalidImageError
from multimodal_agent import __version__
from .logger import get_logger


# Load .env from the project root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(ROOT_DIR, ".env")
load_dotenv(ENV_PATH)

logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent",
        description="Multimodal Agent powered by Google Gemini",
    )
    # parser debug field
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    # parser model field.
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-2.5-flash",
        help="Specify which model to use",
    )
    # parser version field
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version and exit",
    )

    subparsers = parser.add_subparsers(dest="command")

    # agent ask "hello"
    ask_parser = subparsers.add_parser("ask", help="Ask a text-only question")
    ask_parser.add_argument("prompt", type=str, help="Your question")

    # agent image cats.jpg "describe this"
    image_parser = subparsers.add_parser("image", help="Ask with image + text")
    image_parser.add_argument("image_path", type=str, help="Path to local image")
    image_parser.add_argument("prompt", type=str, help="Your question")

    # agent chat.
    subparsers.add_parser("chat", help="Start interactive chat mode")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.version:
        print(f"multimodal-agent version {__version__}")
        return

    if args.debug:
        os.environ["LOGLEVEL"] = "DEBUG"
        logger.setLevel("DEBUG")

    if not args.command:
        parser.print_help()
        return

    # create agent instance
    agent = MultiModalAgent(model=args.model)

    try:
        # asking question in text.
        if args.command == "ask":
            response = agent.ask(args.prompt)
            # chat output.
            print(response)
            return
        # Image questions.
        elif args.command == "image":
            try:
                image_as_part = load_image_as_part(args.image_path)
            except Exception:
                raise InvalidImageError(f"Cannot read image: {args.image_path}")
            response = agent.ask_with_image(args.prompt, image_as_part)
            # chat output.
            print(response)
            return
        # chat mode.
        elif args.command == "chat":
            agent.chat()
            return

    except AgentError as exception:
        logger.error(f"Agent failed: {exception}")
        system.exit(1)
