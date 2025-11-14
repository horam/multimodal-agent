from multimodal_agent.agent_core import MultiModalAgent
from multimodal_agent.utils import load_image_as_part


def test_task_text(mock_agent):
    response = mock_agent.ask("hello")
    assert response == "mocked response"


def test_task_with_image(mock_agent, tmp_path):
    image_path = tmp_path / "img.jpg"
    image_path.write_bytes(b"\xff\xd8\xff\xd9")

    image_part = load_image_as_part(image_path)

    response = mock_agent.ask_with_image("describe", image_part)

    assert response == "mocked response"


def test_chat_history_format(mock_agent, mocker):
    """
    Ensure chat appends text to history correctly.
    """

    # simulate user input twice then exit
    mocker.patch("builtins.input", side_effect=["hello", "exit"])

    # simulate generate_content returning deterministic text
    mock_agent.safe_generate_content = lambda contents: type("R", (), {"text": "reply"})

    # running chat should not raise exceptions
    mock_agent.chat()
