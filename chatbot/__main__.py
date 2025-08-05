"""
Entry point of the game
"""
from chatbot.cli import get_command_line_args
from chatbot.chat_agent import get_weather_data
from chatbot.utils import display_weather_info


def main() -> None:
    """Entry point of the weather application. Gets the command line arguments"""
    args = get_command_line_args()

    weather_data = get_weather_data(args.city, args.imperial)
    display_weather_info(weather_data)


if __name__ == "__main__":
    main()
