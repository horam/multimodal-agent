from unittest.mock import Mock, patch

from multimodal_agent.codegen.generator import CodeGenerator


@patch("multimodal_agent.codegen.generator.find_flutter_root")
def test_init_sets_root(mock_find_root):
    mock_find_root.return_value = "/fake/project"
    agent = Mock()
    generator = CodeGenerator(agent)

    assert generator.root == "/fake/project"
    mock_find_root.assert_called_once_with(".")


@patch("multimodal_agent.codegen.generator.safe_write_file")
@patch("multimodal_agent.codegen.generator.build_widget_prompt")
@patch("multimodal_agent.codegen.generator.widget_file_path")
@patch("multimodal_agent.codegen.generator.find_flutter_root")
def test_generate_widget(
    mock_find_root,
    mock_widget_path,
    mock_build_prompt,
    mock_safe_write,
):
    mock_find_root.return_value = "/project"
    mock_widget_path.return_value = "/project/lib/widgets/test_widget.dart"
    mock_build_prompt.return_value = "PROMPT"

    mock_response = Mock()
    mock_response.text = "   class TestWidget {}   "

    agent = Mock()
    agent.ask.return_value = mock_response

    generator = CodeGenerator(agent)

    result = generator.generate_widget(
        name="test_widget",
        stateful=True,
        override=True,
    )

    mock_widget_path.assert_called_once_with(
        "/project",
        "test_widget",
    )

    mock_build_prompt.assert_called_once_with(
        name="test_widget",
        stateful=True,
    )

    agent.ask.assert_called_once_with("PROMPT")

    mock_safe_write.assert_called_once_with(
        "/project/lib/widgets/test_widget.dart",
        "class TestWidget {}",
        override=True,
    )

    assert result == "/project/lib/widgets/test_widget.dart"


@patch("multimodal_agent.codegen.generator.safe_write_file")
@patch("multimodal_agent.codegen.generator.build_screen_prompt")
@patch("multimodal_agent.codegen.generator.screen_file_path")
@patch("multimodal_agent.codegen.generator.find_flutter_root")
def test_generate_screen(
    mock_find_root,
    mock_screen_path,
    mock_build_prompt,
    mock_safe_write,
):
    mock_find_root.return_value = "/project"
    mock_screen_path.return_value = "/project/lib/screens/home_screen.dart"
    mock_build_prompt.return_value = "SCREEN_PROMPT"

    mock_response = Mock()
    mock_response.text = "   class HomeScreen {}   "

    agent = Mock()
    agent.ask.return_value = mock_response

    generator = CodeGenerator(agent)

    result = generator.generate_screen(
        name="home_screen",
        override=True,
    )

    mock_screen_path.assert_called_once_with("/project", "home_screen")
    mock_build_prompt.assert_called_once_with(name="home_screen")
    agent.ask.assert_called_once_with("SCREEN_PROMPT")

    mock_safe_write.assert_called_once_with(
        "/project/lib/screens/home_screen.dart",
        "class HomeScreen {}",
        override=True,
    )

    assert result.endswith("home_screen.dart")


@patch("multimodal_agent.codegen.generator.safe_write_file")
@patch("multimodal_agent.codegen.generator.build_model_prompt")
@patch("multimodal_agent.codegen.generator.model_file_path")
@patch("multimodal_agent.codegen.generator.find_flutter_root")
def test_generate_model(
    mock_find_root,
    mock_model_path,
    mock_build_prompt,
    mock_safe_write,
):
    mock_find_root.return_value = "/project"
    mock_model_path.return_value = "/project/lib/models/user_model.dart"
    mock_build_prompt.return_value = "MODEL_PROMPT"

    mock_response = Mock()
    mock_response.text = "   class UserModel {}   "

    agent = Mock()
    agent.ask.return_value = mock_response

    generator = CodeGenerator(agent)

    result = generator.generate_model(
        name="user_model",
        override=False,
    )

    mock_model_path.assert_called_once_with("/project", "user_model")
    mock_build_prompt.assert_called_once_with(name="user_model")
    agent.ask.assert_called_once_with("MODEL_PROMPT")

    mock_safe_write.assert_called_once_with(
        "/project/lib/models/user_model.dart",
        "class UserModel {}",
        override=False,
    )

    assert result.endswith("user_model.dart")
