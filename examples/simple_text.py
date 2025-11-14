from dotenv import load_dotenv
from src.multimodal_agent.agent_core import MultiModalAgent

load_dotenv()
agent = MultiModalAgent()

print(agent.ask("Hello! Give me a short inspirational quote."))
