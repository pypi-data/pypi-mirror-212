# Universal Profile Picture
> A CLI app that automatically puts a profile image in all your accounts.

## Installation
```sh
pip install unipropic
unipropic -v # Check if it's working
```
Unipropic supports Python 3.11 and newer.

## Usage
```sh
unipropic <browser> <path-to-the-profile-picture>
```
The supported browsers are Firefox, Chrome, Chromium, Brave [(See below more info)](#custom-binary-path), Edge and Internet Explorer.

### Reliability warning
This app interacts with web pages in a quirky way so it's prone to fail sometimes. To avoid continuous errors in some websites it's recommend to put them in english and set the emerging browser in 16:9 aspect ratio.

### Options
| Flag | Usage |
| - | - |
| `--help`, `-h` | See the help info message. |
| `--version`, `-v` | Shows the current version. |
| `--config-path`, `-c`| Select a custom configuration directory file path. |
| `--forget-config`, `-f` |  Ignore the settings saved for the browser and ask for them again. |
| `--select-services`, `-s` | Select the services to be saved to the configuration file for default use. |
| `--temporal-services`, `-t` | Select the desired services ignoring the ones saved in the configuration file. |
| `--binary-path`, `-b` | Select a custom browser binary path. |

### Custom binary path
Some browsers, like Brave, will fail to start if you install them in a unexpected path. Because of this you can set a custom binary path with `-b` or `--binary-path`.

### Incompatibilities
The compatiblity of this app is determinated by the availability of webdrivers in your platform by the developer of the browser. Due to this, some platforms are not available, such as Chromium on Macs with ARM.

## Author
Created with :heart: by [Kutu](https://kutu-dev.github.io).
> - GitHub - [kutu-dev](https://github.com/kutu-dev)
> - Twitter - [@kutu_dev](https://twitter.com/kutu_dev)
