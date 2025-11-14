import pytest
from multimodal_agent.agent_core import MultiModalAgent


@pytest.fixture
def mock_client_response():
    """
    Fake Gemini response object with .text attribute.
    """

    class Response:
        def __init__(self, text="mocked response"):
            self.text = text

    return Response()


@pytest.fixture
def mock_agent(mocker, mock_client_response):
    """
    Create a MultiModalAgent with a mocked client so no real API calls happen.
    """
    mock_client = mocker.Mock()
    mock_client.models.generate_current.return_value = mock_client_response
    agent = MultiModalAgent(client=mock_client)

    mock_generate = mocker.patch.object(
        agent.client.models, "generate_content", return_value=mock_client_response
    )
    return agent
