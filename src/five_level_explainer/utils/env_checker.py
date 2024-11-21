import os
from colorama import Fore, Style

REQUIRED_ENV_VARS = {
    'OPENAI_API_KEY': 'OpenAI API key',
    'SERPER_API_KEY': 'Serper API key'
}

def color_print(text: str, color: str) -> None:
    """Print text in specified color using colorama.
    
    Args:
        text (str): The text to print
        color (str): Color from colorama.Fore (e.g., 'BLUE', 'RED', 'GREEN')
    """
    color_code = getattr(Fore, color.upper(), Fore.WHITE)  # Default to white if color not found
    print(f"{color_code}{text}{Style.RESET_ALL}")

def is_env_var_set(var_name: str) -> bool:
    """Check if an environment variable is set."""
    return bool(os.getenv(var_name))

def check_required_env_vars() -> list[str]:
    """Return a list of missing required environment variables."""
    return [var for var in REQUIRED_ENV_VARS if not is_env_var_set(var)]

def print_missing_env_vars_message(missing_vars: list[str]) -> None:
    """Print helpful message about missing environment variables."""
    if not missing_vars:
        return
        
    message = "Error: Missing required environment variables:\n"
    message += "".join(f"- {var} ({REQUIRED_ENV_VARS[var]})\n" for var in missing_vars)
    message += "\nPlease set these environment variables before running the application.\n"
    message += "You can set them by:\n"
    message += "1. Creating a .env file in your project root\n"
    message += "2. Setting them in your shell:\n"
    message += "".join(f"   export {var}=your_key_here\n" for var in missing_vars)
    
    print(message, end='')