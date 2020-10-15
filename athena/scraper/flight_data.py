import json
import os

from .chrome_driver import get_chrome_driver
from . import symphony

def get_flight_data(start_date, end_date):
    """ Scrapes the flight data between start_date and end_date"""

    symphony.prepare_directory()

    driver = get_chrome_driver(headless=True)

    driver.get(symphony.url())
    driver.implicitly_wait(20)  # wait a few seconds

    # switch to menu frame
    driver.switch_to.default_content()
    driver.switch_to.frame("MenuFrame")

    # Login
    cred_file = os.path.join( os.environ['ATHENA_CREDENTIALS_PATH'], "harris_reader.json")
    data = json.loads(open(cred_file).read())

    symphony.find_and_set_element_by_name(driver, "txtSystemName", data['system_name'])
    symphony.find_and_set_element_by_name(driver, "txtUserName", data['username'])
    symphony.find_and_set_element_by_name(driver, "txtPassword", data['password'])
    submit = driver.find_element_by_name("submit")
    submit.click()

    # click on reports
    symphony.click_reports(driver)

    # click on custom
    symphony.click_custom(driver)

    # select NREL 
    driver.implicitly_wait(5)  # seconds     
    elem = driver.find_element_by_name("txtSelectedReportName")
    elem.send_keys("_NREL_flights")

    # click on Run Report
    symphony.click_run_report(driver)

    # switch frame
    driver.switch_to.default_content()
    driver.switch_to.frame("ContentFrame")

    symphony.run_report(driver, start_date, end_date)

    filename = symphony.wait_for_download()
    return filename

