# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['unipropic']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.6,<0.5.0',
 'inquirer>=3.1.3,<4.0.0',
 'selenium>=4.8.3,<5.0.0',
 'tomlkit>=0.11.7,<0.12.0',
 'webdriver-manager>=3.8.5,<4.0.0']

entry_points = \
{'console_scripts': ['unipropic = unipropic.main:main']}

setup_kwargs = {
    'name': 'unipropic',
    'version': '1.0.1',
    'description': 'A CLI app that automatically puts a profile image in all your accounts.',
    'long_description': "# Universal Profile Picture\n> A CLI app that automatically puts a profile image in all your accounts.\n\n## Installation\n```sh\npip install unipropic\nunipropic -v # Check if it's working\n```\nUnipropic supports Python 3.11 and newer.\n\n## Usage\n```sh\nunipropic <browser> <path-to-the-profile-picture>\n```\nThe supported browsers are Firefox, Chrome, Chromium, Brave [(See below more info)](#custom-binary-path), Edge and Internet Explorer.\n\n### Reliability warning\nThis app interacts with web pages in a quirky way so it's prone to fail sometimes. To avoid continuous errors in some websites it's recommend to put them in english and set the emerging browser in 16:9 aspect ratio.\n\n### Options\n| Flag | Usage |\n| - | - |\n| `--help`, `-h` | See the help info message. |\n| `--version`, `-v` | Shows the current version. |\n| `--config-path`, `-c`| Select a custom configuration directory file path. |\n| `--forget-config`, `-f` |  Ignore the settings saved for the browser and ask for them again. |\n| `--select-services`, `-s` | Select the services to be saved to the configuration file for default use. |\n| `--temporal-services`, `-t` | Select the desired services ignoring the ones saved in the configuration file. |\n| `--binary-path`, `-b` | Select a custom browser binary path. |\n\n### Custom binary path\nSome browsers, like Brave, will fail to start if you install them in a unexpected path. Because of this you can set a custom binary path with `-b` or `--binary-path`.\n\n### Incompatibilities\nThe compatiblity of this app is determinated by the availability of webdrivers in your platform by the developer of the browser. Due to this, some platforms are not available, such as Chromium on Macs with ARM.\n\n## Author\nCreated with :heart: by [Kutu](https://kutu-dev.github.io).\n> - GitHub - [kutu-dev](https://github.com/kutu-dev)\n> - Twitter - [@kutu_dev](https://twitter.com/kutu_dev)\n",
    'author': 'kutu-dev',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
