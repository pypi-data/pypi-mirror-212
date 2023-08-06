import sys
from colorama import Fore, Style

class Messages():
    @staticmethod
    def error(message: str) -> None:
        """Prints the desired error message decorated and ends the execution of the program"""

        print(f'[ {Fore.RED}ERROR{Style.RESET_ALL} ] {message}')
        sys.exit(1)

    def warn(message: str) -> None:
        """Prints the desired warn message decorated"""

        print(f'[ {Fore.YELLOW}WARN{Style.RESET_ALL} ] {message}')

    def info(message: str) -> None:
        """Prints the desired info message decorated"""

        print(f'[ {Fore.BLUE}INFO{Style.RESET_ALL} ] {message}')

    def format_argument(argument: str) -> str:
        """Return the given argument colored with green and with apostrophes"""

        return f'{Fore.GREEN}\'--{argument}\'{Style.RESET_ALL}'