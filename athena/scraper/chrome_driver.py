import os
import requests
import zipfile
import io
from sys import platform as _platform

from selenium.webdriver import ChromeOptions
from seleniumrequests import Chrome

def get_chrome_driver(headless=True):
    """ Get the instantiated chrome driver"""
    executable_path = ensure_chrome_driver()
    options = get_chrome_options(headless=headless)
    driver = Chrome(options=options, executable_path=executable_path)   
    enable_download_in_headless_chrome(driver, os.getcwd())
    return driver

def get_chrome_options(headless=False):
    """ Return options for chrome driver"""
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument('headless')
        chrome_options.add_argument('no-sandbox')
        chrome_options.add_argument('disable-dev-shm-usage')
        chrome_options.add_argument('disable-gpu')
    return chrome_options

def enable_download_in_headless_chrome(browser, download_dir):
    """ Add missing support for chrome "send_command"  to selenium webdriver
        This enables a headless download.
        Grabbed from stack overflow.
    """
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

def ensure_chrome_driver():
    """ Download, if necessary, the chrome executable """
    CHROME_DRIVER_VERSION = 2.41
    CHROME_DRIVER_BASE_URL = 'https://chromedriver.storage.googleapis.com/{}/chromedriver_{}.zip'
    CHROME_ZIP_TYPES = {
        'linux': 'linux64',
        'linux2': 'linux64',
        'darwin': 'mac64',
        'win32': 'win32',
        'win64': 'win32'
    }
    
    zip_type = CHROME_ZIP_TYPES.get(_platform)
    executable_path = os.getcwd() + os.path.sep + 'chromedriver'

    if not os.path.exists(executable_path):
        zip_file_url = CHROME_DRIVER_BASE_URL.format(CHROME_DRIVER_VERSION, zip_type)
        request = requests.get(zip_file_url)

        if request.status_code != 200:
            msg = 'Error finding chromedriver at {}, status = {}'
            raise RuntimeError(msg.format(zip_file_url, request.status_code))

        zip_file = zipfile.ZipFile(io.BytesIO(request.content))
        zip_file.extractall()
        os.chmod(executable_path, 0o755)

    return executable_path