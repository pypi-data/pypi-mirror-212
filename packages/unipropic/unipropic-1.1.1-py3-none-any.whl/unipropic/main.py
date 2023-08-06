import sys
from . import __version__, APP_NAME, MINIFIED_APP_NAME
from .messages import Messages
from .config_manager import ConfigManager
from .webdriver_handlers import ChromeBasedProfilePictureHandler, ChromeVariant, EdgeProfilePictureHandler, FirefoxProfilePictureHandler, InternetExplorerPictureHandler
from typing import Any, Sequence
import inquirer
import argparse
from pathlib import Path
from colorama import Fore, Style

class VersionAction(argparse.Action):
    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: str | Sequence[Any] | None, option_string: str | None = None) -> None:
        Messages.info(f'{APP_NAME} {__version__}')
        parser.exit()

def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog=MINIFIED_APP_NAME,
        description=f'{APP_NAME} - Unifies your profile picture browsing and changing them for you with your browser',
        epilog='Created with ♥ by Kutu (https://kutu-dev.github.io/)'
    )

    parser.add_argument(
        '-v',
        '--version',
        action=VersionAction,
        nargs=0,
        default=False,
        help=f'shows the current version of {MINIFIED_APP_NAME}'
    )

    parser.add_argument(
        '-f',
        '--forget-config',
        action='store_true',
        default=False,
        help='ignore the settings saved for the browser and ask for them again'
    )

    parser.add_argument(
        '-c',
        '--config-path',
        metavar='path',
        default=None,
        type=Path,
        help='select a custom configuration directory file path'
    )

    parser.add_argument(
        '-s',
        '--select-services',
        action='store_true',
        default=False,
        help='select the services to be saved to the configuration file for default use'
    )

    parser.add_argument(
        '-t',
        '--temporal-services',
        action='store_true',
        default=False,
        help='select the desired services ignoring the ones saved in the configuration file'
    )

    parser.add_argument(
        'browser',
        choices=['firefox', 'chrome', 'chromium', 'brave', 'edge', 'ie'],
        type=str.lower,
        nargs='+',
        help='select the browser to use'
    )

    parser.add_argument(
        '-b',
        '--binary-path',
        metavar='path',
        default="",
        type=str,
        help='select a custom browser binary path'
    )

    parser.add_argument(
        'picture_path',
        type=Path,
        metavar='picture-path',
        help='the path to the new profile picture'
    )

    args: argparse.Namespace = parser.parse_args()

    if len(args.browser) != 1:
        Messages.error('You can\'t select more than one browser')

    if args.select_services and args.temporal_services:
        Messages.error(f'You can\'t have {Messages.format_argument("selected-service")} and {Messages.format_argument("temporal-services")} selected at the same time')

    config_manager: ConfigManager = ConfigManager(MINIFIED_APP_NAME, args.config_path)

    print(f'Welcome to {Fore.BLUE}{APP_NAME}{Style.RESET_ALL}')

    match args.browser[0]:
        case 'firefox':
            handler: FirefoxProfilePictureHandler = FirefoxProfilePictureHandler(
                args.picture_path,
                config_manager,
                args.forget_config,
                args.binary_path
            )
        case 'chrome':
            handler: ChromeBasedProfilePictureHandler = ChromeBasedProfilePictureHandler(
                args.picture_path,
                config_manager,
                ChromeVariant.GOOGLE,
                args.binary_path
            )
        case 'chromium':
            handler: ChromeBasedProfilePictureHandler = ChromeBasedProfilePictureHandler(
                args.picture_path,
                config_manager,
                ChromeVariant.CHROMIUM,
                args.binary_path
            )
        case 'brave':
            handler: ChromeBasedProfilePictureHandler = ChromeBasedProfilePictureHandler(
                args.picture_path,
                config_manager,
                ChromeVariant.BRAVE,
                args.binary_path
            )
        case 'edge':
            handler: EdgeProfilePictureHandler = EdgeProfilePictureHandler(
                args.picture_path,
                config_manager,
                args.binary_path
            )
        case 'ie':
            handler: InternetExplorerPictureHandler = InternetExplorerPictureHandler(
                args.picture_path,
                config_manager,
                args.binary_path
            )
    
    # Avoid having improper closed Webdriver sessions
    try:
        active_services: list[str] | None = config_manager.get_value_by_key('services')

        if active_services == None or len(active_services) == 0 or args.select_services or args.temporal_services:
            available_services = list(handler.services.keys())

            try:
                active_services: str = inquirer.prompt([
                    inquirer.Checkbox(
                    'selected_services',
                    'Which services you want to automatize?',
                    available_services
                   )
                ])['selected_services']
            except TypeError:
                sys.exit(1)

            if len(active_services) == 0:
                Messages.error('No services has been selected')

            if not args.temporal_services:
                config_manager.set_value_by_key('services', active_services)
                Messages.info(f'selected services saved as default, you can change them with {Messages.format_argument("select-services")}')

        for service in active_services:
            try:
                handler.services[service]()
            except KeyError:
                # Detect and delete services that does not exists and remove them from the config
                active_services.remove(service)
                if not args.temporal_services:
                    config_manager.set_value_by_key('services', active_services)

        Messages.info(f'{len(handler.succeed_services)} of {len(handler.succeed_services)+len(handler.failed_services)} services have been applied successfully')

        if len(handler.failed_services) == 1:
            Messages.warn(f'The service {handler.failed_services[0]} has failed')

        if len(handler.failed_services) > 1:
            Messages.warn(f'The services {" ".join(handler.failed_services[0:-1])} and {handler.failed_services[-1]} have failed')
    finally:
        # End execution of the program and close the browser deleting all the temp files in the process
        handler.driver.quit()
