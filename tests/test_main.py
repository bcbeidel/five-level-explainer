import pytest
from five_level_explainer.main import print_missing_env_vars_message

def test_print_missing_env_vars_message(capsys):
    # Arrange
    missing_vars = ['OPENAI_API_KEY', 'SERPER_API_KEY']
    expected_output = """Error: Missing required environment variables:
- OPENAI_API_KEY (OpenAI API key)
- SERPER_API_KEY (Serper API key)

Please set these environment variables before running the application.
You can set them by:
1. Creating a .env file in your project root
2. Setting them in your shell:
   export OPENAI_API_KEY=your_key_here
   export SERPER_API_KEY=your_key_here
"""

    # Act
    print_missing_env_vars_message(missing_vars)
    captured = capsys.readouterr()

    # Assert
    assert captured.out == expected_output

def test_print_missing_env_vars_message_single_var(capsys):
    # Arrange
    missing_vars = ['OPENAI_API_KEY']
    expected_output = """Error: Missing required environment variables:
- OPENAI_API_KEY (OpenAI API key)

Please set these environment variables before running the application.
You can set them by:
1. Creating a .env file in your project root
2. Setting them in your shell:
   export OPENAI_API_KEY=your_key_here
   export SERPER_API_KEY=your_key_here
"""

    # Act
    print_missing_env_vars_message(missing_vars)
    captured = capsys.readouterr()

    # Assert
    assert captured.out == expected_output 