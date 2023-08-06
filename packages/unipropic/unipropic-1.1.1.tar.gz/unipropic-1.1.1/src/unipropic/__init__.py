__version__: str = '1.1.1'
APP_NAME: str = 'Universal Profile Picture'
MINIFIED_APP_NAME = 'unipropic'

# Disable visible download progress bar of webdriver_manager
import os
os.environ['WDM_PROGRESS_BAR'] = str(0)

# Start colorama Windows compatibly
import colorama
colorama.just_fix_windows_console()
