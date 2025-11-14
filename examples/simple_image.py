"""
Usage:
    python examples/simple_image.py ./cat.jpg "Describe this image"
"""

import sys
from dotenv import load_dotenv

from src.multimodal_agent.agent_core import MultiModalAgent
from src.multimodal_agent.utils import load_image_as_part


def main():
    if len(sys.argv) < 3:
        print('Usage: python simple_image.py <img_path> "prompt"')
        return

    img_path = sys.argv[1]
    prompt = " ".join(sys.argv[2:])

    agent = MultiModalAgent()
    image = load_image_as_part(img_path)

    print(agent.ask_with_image(prompt, image))


if __name__ == "__main__":
    load_dotenv()
    main()
