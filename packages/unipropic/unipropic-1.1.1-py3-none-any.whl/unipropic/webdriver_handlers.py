from configparser import ConfigParser
import sys
from .config_manager import ConfigManager
from .messages import Messages
import platform
import inquirer
from enum import Enum
from abc import abstractmethod, ABC
import time
from typing import Callable
from colorama import Fore, Style
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager
from pathlib import Path

class ProfilePictureHandler(ABC):
    """Manipulates the websites to change the profile picture to the desired one"""

    def __init__(self, profile_picture_path: Path, config_manager: ConfigManager) -> None:
        self.profile_picture_path: str = str(profile_picture_path.absolute())
        self.config_manager = config_manager

        # Creates the driver using an abstract method
        self.driver = self.create_driver()

        # Create wait object with a timeout of 20 seconds
        self.wait = WebDriverWait(self.driver, 20, poll_frequency=1)

        self.services: dict[str, Callable] = {
            'Reddit': self.change_in_reddit,
            'GitHub': self.change_in_github,
            'Twitter': self.change_in_twitter,
            'Google': self.change_in_google,
            'Twitch': self.change_in_twitch,
            'Steam': self.change_in_steam,
            'Instagram': self.change_in_instagram,
            'Gravatar': self.change_in_gravatar,
            'Discord': self.change_in_discord,
            'Firefox': self.change_in_firefox,
            'Backloggd': self.change_in_backloggd,
            'Letterboxd': self.change_in_letterboxd,
            'Anilist': self.change_in_anilist,
            'Serializd': self.change_in_serializd,
            'WhatsApp': self.change_in_whatsapp,
            'Microsoft': self.change_in_microsoft,
            'Apple': self.change_in_apple,
            'Xiaomi': self.change_in_xiaomi
        }

        self.succeed_services: list[str] = []
        self.failed_services: list[str] = []

    @abstractmethod
    def create_driver(self) -> webdriver.Remote | webdriver.Firefox | webdriver.Chrome | webdriver.Ie | webdriver.Safari | webdriver.WebKitGTK | webdriver.Edge | webdriver.ChromiumEdge:
        """Returns the WebDriver object to use"""

    def service_with_result(name_of_the_service: str) -> None:
        def inner(function: Callable) -> None:
            def wrapper(self, *args, **kwargs) -> None:
                """Call the function passed and prints if it has success or not"""
                justify: int = 40-len(name_of_the_service)

                print(f' {name_of_the_service}...', end="")
                print(f'[ {Fore.YELLOW}WORKING{Style.RESET_ALL} ]'.rjust(justify), end="\r")
                try:
                    function(self, *args, **kwargs)
                except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as exception_message:
                    print(f' {name_of_the_service}...', end="")
                    print(f'[ {Fore.RED}FAIL{Style.RESET_ALL} ]'.rjust(justify))
                    print(f'   {Fore.YELLOW}Hint:{Style.RESET_ALL} Maybe you haven\'t logged in on {name_of_the_service}'.rjust(justify))
                    self.failed_services.append(name_of_the_service)
                    self.config_manager.write_into_log(f'[ ERROR ] Service {name_of_the_service} has failed:\n{exception_message}')
                else:
                    print(f' {name_of_the_service}...', end="")
                    print(f'[ {Fore.GREEN}SUCCESS{Style.RESET_ALL} ]'.rjust(justify))
                    self.succeed_services.append(name_of_the_service)
                    self.config_manager.write_into_log(f'[ INFO ] Service {name_of_the_service} applied successfully')
            return wrapper
        return inner

    def drag_and_drop_file(self, element, file_to_drop_path) -> None:
        """Emulates drag and drop of a file to a specific element"""

        js_emulate_drag_and_drop = """
            var target = arguments[0],
            offsetX = arguments[1],
            offsetY = arguments[2],
            document = target.ownerDocument || document,
            window = document.defaultView || window;

            var input = document.createElement('INPUT');
            input.type = 'file';
            input.onchange = function () {
            var rect = target.getBoundingClientRect(),
                x = rect.left + (offsetX || (rect.width >> 1)),
                y = rect.top + (offsetY || (rect.height >> 1)),
                dataTransfer = { files: this.files };

              ['dragenter', 'dragover', 'drop'].forEach(function (name) {
                var evt = document.createEvent('MouseEvent');
                evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
                evt.dataTransfer = dataTransfer;
                target.dispatchEvent(evt);
              });

              setTimeout(function () { document.body.removeChild(input); }, 25);
            };
            document.body.appendChild(input);
            return input;
        """

        file_input = self.driver.execute_script(js_emulate_drag_and_drop, element, 0, 0)
        file_input.send_keys(file_to_drop_path)

    @service_with_result('Reddit')
    def change_in_reddit(self) -> None:
        """Change the profile picture in Reddit"""

        self.driver.get('https://www.reddit.com/settings/profile')
        picture_input = self.driver.find_element(By.XPATH, '//div[@class="_3oOZrOdvGjAOYvzKCu-Kjf"]/input')
        picture_input.send_keys(self.profile_picture_path)
        
        # Wait until the image is loaded to the website
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="LoadingIcon"]')))
        time.sleep(1)
        self.wait.until_not(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="LoadingIcon"]')))

    @service_with_result('GitHub')
    def change_in_github(self) -> None:
        """Change the profile picture in GitHub"""

        self.driver.get('https://github.com/settings/profile')
        picture_input = self.driver.find_element(By.XPATH, '//input[@id="avatar_upload"]')
        picture_input.send_keys(self.profile_picture_path)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//form[@id="avatar-crop-form"]/div[@class="Box-footer"]/button[@name="op"]'))).click()

    @service_with_result('Twitter')
    def change_in_twitter(self) -> None:
        """Change the profile picture in Twitter"""

        self.driver.get('https://twitter.com/settings/profile')
        
        # Wait until the profile edit menu loads
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Add avatar photo"]')))

        picture_input = self.driver.find_element(By.XPATH, '//div[div[@aria-label="Add avatar photo"]]/input[@type="file"]')
        picture_input.send_keys(self.profile_picture_path)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="applyButton"]'))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="Profile_Save_Button"]'))).click()

        self.wait.until_not(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="Profile_Save_Button"]')))

        # Wait until the website process the image
        time.sleep(1)

    @service_with_result('Google')
    def change_in_google(self) -> None:
        """Change the profile picture in Google"""

        self.driver.get('https://myaccount.google.com/personal-info')

        # Profile picture popup button
        self.driver.find_element(By.XPATH, '//div[@jscontroller="nEO8Ne"]').click()

        self.driver.switch_to.frame(
            self.driver.find_element(By.XPATH, '//iframe[@style="inset: 0px; position: fixed; border: medium none; height: 100%; width: 100%; z-index: 2001;"]')
        )

        # Change profile picture button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="ZMAVtd"]'))).click()

        # Wait for the change window size animation to end
        time.sleep(1)

        # Go to 'From computer' upload section
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="nTuXNc"]'))).click()

        self.drag_and_drop_file(self.driver.find_element(By.XPATH, '//div[@class="cevIvf"]'), self.profile_picture_path)

        # Wait until the image is processed and the button 'Next' is enabled
        self.wait.until_not(EC.invisibility_of_element_located((By.XPATH, '//button[@jslog="89765; track:click"]')))

        # Wait for loading animation to end
        time.sleep(2)
        
        self.driver.find_element(By.XPATH, '//button[@jslog="89765; track:click"]').click()

        # Wait for loading animation to end
        time.sleep(1)
        
        self.driver.find_element(By.XPATH, '//button[@jslog="163906; track:click"]').click()

        self.driver.switch_to.default_content()

    @service_with_result('Twitch')
    def change_in_twitch(self) -> None:
        """Change the profile picture in Twitch"""

        self.driver.get('https://www.twitch.tv/settings/profile')

        # Wait until the profile picture loads and all the website is interactive
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//img[@alt="Profile Picture"]')))

        picture_input = self.driver.find_element(By.XPATH, '//input[@class="profile-image-setting__input"]')
        picture_input.send_keys(self.profile_picture_path)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text() = "Save"]'))).click()

        # Wait until the popup 'Successfully updated your profile picture.' appears
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="Layout-sc-1xcs6mc-0 lpkbps"]')))

    @service_with_result('Steam')
    def change_in_steam(self) -> None:
        """Change the profile picture in Steam"""

        self.driver.get('https://steamcommunity.com/id/Kutu__/edit/avatar')

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text() = "Upload your avatar"]')))

        picture_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
        picture_input.send_keys(self.profile_picture_path)

        # Wait for the picture to be processed
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="avatarcrop_AvatarCrop_UVQKc"]')))

        self.driver.find_element(By.XPATH, '//button[text() = "Save"]').click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="DialogButton _DialogLayout Primary Disabled Focusable"]')))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="DialogButton _DialogLayout Primary Focusable"]')))

    @service_with_result('Instagram')
    def change_in_instagram(self) -> None:
        """Change the profile picture in Instagram"""

        self.driver.get('https://www.instagram.com/accounts/edit')

        # Wait until the profile picture has loaded and the website is ready to use
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//img[@class="_aadp"]')))

        picture_input = self.driver.find_element(By.XPATH, '//input[@class="_ac69"]')
        picture_input.send_keys(self.profile_picture_path)

        # Wait until the popup 'Profile photo added.' appears
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="_acb3"]')))

    @service_with_result('Gravatar')
    def change_in_gravatar(self) -> None:
        """Change the profile picture in Gravatar"""

        self.driver.get('https://gravatar.com/emails')

        # Selenium does not allow to interact with any element in a list of elements if the webpage reloads itself
        # As this service should removes previous used pictures in Gravatar the only way to do it's try to click the remove button until the are no more available
        while True:
            time.sleep(1)
            delete_previous_pictures_buttons = self.driver.find_elements(By.XPATH, '//div[@class="delete"]/a')

            if len(delete_previous_pictures_buttons) == 0:
                break

            delete_previous_pictures_buttons[0].click()
            self.wait.until(EC.alert_is_present()).accept()

        picture_input = self.driver.find_element(By.XPATH, '//input[@id="gravatar_file"]')
        picture_input.send_keys(self.profile_picture_path)

        zoom_down_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="crop-ctrl-zoom-down"]')))

        # Wait until the website process the image
        time.sleep(2)

        # Zoom out the image 11 times to make it fit the image cropper
        for _ in range(11):
            zoom_down_button.click()
            time.sleep(0.2)

        crop_button = self.driver.find_element(By.XPATH, '//button[@id="do-crop"]')
        crop_button.click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="gravatar_rating_container"]/*/input'))).click()

    @service_with_result('Discord')
    def change_in_discord(self) -> None:
        """Change the profile picture in Discord"""

        self.driver.get('https://discord.com/app')

        settings_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="User Settings"]')))
        
        # Wait until the animation of loading the app ends
        time.sleep(1)

        settings_button.click()

        # Wait until the animation of changing menus ends
        time.sleep(1)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Profiles"]'))).click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="avatarUploaderNormal-2m2hFm avatarUploader-qEFQS2"]'))).click()
        
        # Wait until the animation of changing menus ends
        time.sleep(1)
        
        picture_input = self.driver.find_element(By.XPATH, '//input[@class="file-input"]')
        picture_input.send_keys(self.profile_picture_path)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text() = "Apply"]'))).click()

        # Wait until the animation of changing menus ends
        time.sleep(1)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="button-ejjZWC lookFilled-1H2Jvj colorGreen-jIPCAS sizeSmall-3R2P2p grow-2T4nbg"]'))).click()

        self.wait.until_not(EC.element_to_be_clickable((By.XPATH, '//button[@class="button-ejjZWC lookFilled-1H2Jvj colorGreen-jIPCAS sizeSmall-3R2P2p grow-2T4nbg"]')))

    @service_with_result('Firefox')
    def change_in_firefox(self) -> None:
        """Change the profile picture in Firefox"""

        self.driver.get('https://accounts.firefox.com/settings/avatar')

        picture_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@data-testid="avatar-image-upload-input"]')))
        picture_input.send_keys(self.profile_picture_path)

        # Wait until the website process the image
        time.sleep(1)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="save-button"]'))).click()

        # Wait until the website redirects to the main settings page
        self.wait.until(lambda driver: driver.current_url == "https://accounts.firefox.com/settings#profile-picture")

    @service_with_result('Backloggd')
    def change_in_backloggd(self) -> None:
        """Change the profile picture in Backloggd"""

        self.driver.get('https://www.backloggd.com/settings/')

        picture_input = self.driver.find_element(By.XPATH, '//input[@id="user_avatar_btn"]')
        picture_input.send_keys(self.profile_picture_path)

        # Wait until the website process the image
        self.wait.until_not(EC.element_to_be_clickable((By.XPATH, '//span[@id="file-selected" and text() = ""]')))

        self.driver.find_element(By.XPATH, '//button[@id="save-profile-btn"]').click()

        # Wait until the popup 'Profile successfully updated' appears
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="toast-container"]')))

    @service_with_result('Letterboxd')
    def change_in_letterboxd(self) -> None:
        """Change the profile picture in Letterboxd"""

        self.driver.get('https://letterboxd.com/settings/avatar/')

        # Wait until the webpage creates the input for the profile picture
        time.sleep(1)

        picture_input = self.driver.find_element(By.XPATH, '//input[@id="file-upload"]')
        picture_input.send_keys(self.profile_picture_path)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-js-trigger="save"]'))).click()

        # Wait until the popup 'Your avatar has been updated.' appears
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="jnotify-message"]')))

    @service_with_result('Anilist')
    def change_in_anilist(self) -> None:
        """Change the profile picture in Anilist"""

        self.driver.get('https://anilist.co/settings')

        time.sleep(1)

        picture_input = self.driver.find_element(By.XPATH, '//input[@name="avatar"]')
        picture_input.send_keys(self.profile_picture_path)

        # Wait until the popup 'Avatar updated' appears
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="alert"]')))

    @service_with_result('Serializd')
    def change_in_serializd(self) -> None:
        """Change the profile picture in Serializd"""

        self.driver.get('https://www.serializd.com/settings')

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//img[@class="avatar-image"]')))

        time.sleep(1)

        picture_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
        picture_input.send_keys(self.profile_picture_path)

        # Wait until the popup 'Image uploaded' appears
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text() = "Image uploaded"]')))

    @service_with_result('WhatsApp')
    def change_in_whatsapp(self) -> None:
        """Change the profile picture in WhatsApp"""

        self.driver.get('https://web.whatsapp.com/')

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//header/div/div[@role="button"]'))).click()

        # Wait for the animation to end
        time.sleep(1)

        picture_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
        picture_input.send_keys(self.profile_picture_path)

        zoom_down_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="crop-tool-zoom-out"]')))

        for _ in range(5):
            zoom_down_button.click()
            time.sleep(0.2)

        self.driver.find_element(By.XPATH, '//div[@aria-label="Submit image"]').click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text() = "Profile photo set"]')))

    @service_with_result('Microsoft')
    def change_in_microsoft(self) -> None:
        """Change the profile picture in Microsoft"""
        
        self.driver.get('https://account.microsoft.com/profile/')

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-bi-id="profile.profile-page.profile-pic-section.edit-picture"]'))).click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-bi-id="profile.edit-picture.upload-button"]'))).click()

        picture_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
        picture_input.send_keys(self.profile_picture_path)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-bi-id="profile.edit-picture.save-button"]'))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-bi-id="profile.edit-picture.celebration.close-button-in-dialog-footer"]'))).click()

    @service_with_result('Apple')
    def change_in_apple(self) -> None:
        """Change the profile picture in Apple"""

        self.driver.get('https://www.icloud.com/settings/')

        time.sleep(1)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ui-button[text()[contains(.,"Change Apple ID Photo")]]'))).click()

        print(2)
        picture_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
        picture_input.send_keys(self.profile_picture_path)

        time.sleep(1)

        print(3)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//ui-button[text() = "Save"]'))).click()
        print(4)
        self.wait.until_not(EC.element_to_be_clickable((By.XPATH, '//ui-button[text() = "Save"]')))

    @service_with_result('Xiaomi')
    def change_in_xiaomi(self) -> None:
        """Change the profile picture in Xiaomi"""

        self.driver.get('https://account.xiaomi.com/fe/service/account/profile')

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[text() = "Change"]'))).click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//img[@class="_-src-portals-desktop-pages-Account-pages-Profile-avatar_image"]'))).click()

        picture_input = self.driver.find_element(By.XPATH, '//input[@type="file"]')
        picture_input.send_keys(self.profile_picture_path)

        # Wait for the animation to end
        time.sleep(2)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text() = "Submit"]'))).click()

        # Wait for the animation to end
        time.sleep(2)

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text() = "Save"]'))).click()

        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="_-src-components-LoadingIcon-loadingIcon"]')))
        self.wait.until_not(EC.element_to_be_clickable((By.XPATH, '//span[@class="_-src-components-LoadingIcon-loadingIcon"]')))

class FirefoxProfilePictureHandler(ProfilePictureHandler):
    def __init__(self, profile_picture_path: Path, config_manager: ConfigManager, forget_config: bool, binary_path: str = "") -> None:
        self.forger_config: bool = forget_config
        self.binary_path: str = binary_path

        super().__init__(profile_picture_path, config_manager)

    def get_firefox_profiles_path(self) -> Path:
        """Return the path were Firefox storage the profile directories depending of the OS"""

        match platform.system():
            case 'Windows':
                return Path(
                    Path.home(),
                    'AppData',
                    'Roaming',
                    'Mozilla',
                    'Firefox',
                    'Profiles',
                )
            case 'Darwin':
                return Path(
                    Path.home(),
                    'Library',
                    'Application Support',
                    'Firefox',
                    'Profiles',
                )
            case _:
                return Path(
                    Path.home(),
                    '.mozilla',
                    'firefox',
                )

    def get_firefox_profiles(self) -> list[str]:
        """Return a list to the paths to all the firefox profiles that has been found"""

        profiles_file_path: Path = Path(self.get_firefox_profiles_path(), 'profiles.ini')

        if not profiles_file_path.is_file():
            return []

        profiles_data: ConfigParser = ConfigParser()
        profiles_data.read(profiles_file_path)

        profiles_paths: list[str] = []

        for i in profiles_data:
            if ('Locked', '1') in profiles_data[i].items():
                continue

            if not 'Path' in profiles_data[i]:
                continue

            profiles_data[i].items()
            profiles_paths.append(profiles_data[i]['Path'])

        return profiles_paths

    def ask_for_profile_path(self) -> str:
        """Ask for a valid directory to be used as a profile path"""

        while True:
            firefox_profile_path: Path = Path(input('- Firefox profile path: '))
            
            if firefox_profile_path.is_dir():
                return firefox_profile_path
            
            Messages.warn('The given profile path does not exists or it\'s invalid, please enter a valid one')

    def ask_for_profile(self) -> str:
        firefox_profiles: list[Path] = self.get_firefox_profiles()
        firefox_profiles.append('Manually select profile path...')

        if len(firefox_profiles) == 0:
            Messages.warn('No Firefox profile has been found, please enter it manually')
            return self.ask_for_profile_path()

        try:
            selected_profile: str = inquirer.prompt([
                inquirer.List(
                    'selected_profile',
                    'Please select a Firefox profile',
                    choices=firefox_profiles
                )
            ])['selected_profile']
        except TypeError:
                sys.exit(1)

        if selected_profile == 'Manually select profile path...':
            return self.ask_for_profile_path()
        
        firefox_profile_path = Path(self.get_firefox_profiles_path(), selected_profile)

        if not firefox_profile_path.is_dir():
            Messages.error('The selected profile path does not exists or it\'s invalid, please enter a valid one manually')
            return self.ask_for_profile_path()
        
        return firefox_profile_path

    def create_driver(self) -> webdriver.Firefox:
        """Creates a Firefox Webdriver using the Profile defined in the configuration file"""

        Messages.info('Starting Firefox Webdriver...')

        firefox_profile_path: Path | None

        try:
            firefox_profile_path = Path(self.config_manager.get_value_by_key('firefox'))
        except TypeError:
            firefox_profile_path = None

        if firefox_profile_path == None or not firefox_profile_path.is_dir() or self.forger_config:
            firefox_profile_path = Path(self.get_firefox_profiles_path(), self.ask_for_profile())
        
            Messages.info(f'Profile saved as default, you can reset it using {Messages.format_argument("forget-config")}')
            self.config_manager.set_value_by_key('firefox', str(firefox_profile_path))
        
        service: FirefoxService = FirefoxService(GeckoDriverManager().install())
        options: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
        options.binary_location = self.binary_path
        profile: webdriver.FirefoxProfile = webdriver.FirefoxProfile(firefox_profile_path)

        return webdriver.Firefox(service=service, options=options, firefox_profile=profile)

class ChromeVariant(Enum):
    GOOGLE = {'display_name': 'Chrome', 'chrome_type': ChromeType.GOOGLE}
    CHROMIUM = {'display_name': 'Chromium', 'chrome_type': ChromeType.CHROMIUM}
    BRAVE = {'display_name': 'Brave', 'chrome_type': ChromeType.BRAVE}

class ChromeBasedProfilePictureHandler(ProfilePictureHandler):
    def __init__(self, profile_picture_path: Path, config_manager:ConfigManager, chrome_variant: ChromeVariant, binary_path: str = "") -> None:
        self.chrome_variant: ChromeVariant = chrome_variant
        self.binary_path: str = binary_path

        super().__init__(profile_picture_path, config_manager)

    def create_driver(self) -> webdriver.Chrome:
        """Creates a Chrome based Webdriver"""

        Messages.info(f'Starting {self.chrome_variant.value["display_name"]} Webdriver...')

        service: ChromeService = ChromeService(ChromeDriverManager(chrome_type=self.chrome_variant.value['chrome_type']).install())
        options: webdriver.ChromeOptions = webdriver.ChromeOptions()
        options.binary_location = self.binary_path

        return webdriver.Chrome(service=service, options=options)

class EdgeProfilePictureHandler(ProfilePictureHandler):
    def __init__(self, profile_picture_path: Path, config_manager: ConfigManager, binary_path: str = "") -> None:
        self.binary_path: str = binary_path
        
        super().__init__(profile_picture_path, config_manager)

    def create_driver(self) -> webdriver.Edge:
        """Creates a Edge Webdriver"""

        Messages.info(f'Starting Edge Webdriver...')

        service: EdgeService = EdgeService(EdgeChromiumDriverManager().install())
        options: webdriver.EdgeOptions = webdriver.EdgeOptions()
        options.binary_location = self.binary_path

        return webdriver.Edge(service=service, options=options)

class InternetExplorerPictureHandler(ProfilePictureHandler):
    def __init__(self, profile_picture_path: Path, config_manager: ConfigManager, binary_path: str = "") -> None:
        self.binary_path: str = binary_path

        super().__init__(profile_picture_path, config_manager)

    def create_driver(self) -> webdriver.Ie:
        """Creates a Internet Explorer Webdriver"""

        Messages.info(f'Starting Internet Explorer Webdriver...')

        service: IEService = IEService(IEDriverManager().install())
        options: webdriver.IeOptions = webdriver.IeOptions()
        options.binary_location = self.binary_path

        return webdriver.Ie(service=service, options=options)
