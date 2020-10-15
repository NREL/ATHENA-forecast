import os
import glob
import time

def url():
    return "https://secure.symphonycdm.com"

def find_and_set_element_by_name(driver, name, value):
    elem = driver.find_element_by_name(name)
    elem.clear()
    elem.send_keys(value)

def click_reports(driver):
    """Click on the reports menu"""
    driver.implicitly_wait(5)  # seconds
    for row in driver.find_elements_by_xpath("//td"):
        onclick_text = row.get_attribute('onclick')
        print(onclick_text)
        if onclick_text=="javascript:GoModule('ReportsMenu.asp','')":
            row.click()
            break

def click_custom(driver):
    driver.implicitly_wait(5)  # seconds
    for row in driver.find_elements_by_xpath("//td"):
        onclick_text = row.get_attribute('onclick')
        print(onclick_text)
        if onclick_text=="javascript:CustomReport()":
            row.click()
            break

def click_run_report(driver):
    driver.implicitly_wait(5)  # seconds
    for row in driver.find_elements_by_xpath("//td"):
        onclick_text = row.get_attribute('onclick')
        print(onclick_text)
        if onclick_text=="javascript:RunReport()":
            row.click()
            break

def run_report(driver, start_date, end_date):
    ele = driver.find_element_by_name("txtStartDate")
    ele.clear()
    ele.send_keys(start_date)

    ele = driver.find_element_by_name("txtEndDate")
    ele.clear()
    ele.send_keys(end_date)

    for row in driver.find_elements_by_xpath("//input"):
        if row.get_attribute("value") == "Excel":
            row.click()
            break

    # download 
    run = driver.find_element_by_name("btnRun")
    run.click()

def prepare_directory():
    filenames = glob.glob("*.csv")
    for filename in filenames:
        os.remove(filename)


def wait_for_download(wait_time=30):
    """ Wait a maximum of 20 seconds for the file"""
    count = 0
    while True:
        filenames = glob.glob("*.csv")
        if len(filenames)>0:
            return filenames[0]
        time.sleep(1)
        count += 1
        if count > wait_time:
            break

    