#!/usr/bin/env python3

import string
import datetime
import time
from selenium import webdriver

# UI Test of AWSome SAM App with Chromium and save a screenshot

chrome_options = webdriver.ChromeOptions()
#chrome_options.binary_location = '/opt/headless-chromium'
chrome_options.add_argument('--window-size={}x{}'.format(1280, 1024))
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--disable-dev-shm-usage')

today = datetime.datetime.now()
date = today.strftime("%b-%d-%Y")

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://dlod02c3c462c.cloudfront.net")
driver.save_screenshot(f"{date}_UITest_blank.png")
driver.find_element_by_xpath('//*[@id="First_Name"]').send_keys('Harry')
driver.find_element_by_xpath('//*[@id="Surname"]').send_keys('Potter')
driver.find_element_by_xpath('//*[@id="Email"]').send_keys('hpotter@hogwarts.uk')
driver.find_element_by_xpath('//*[@id="Contact_Number"]').send_keys('07496589430')
driver.save_screenshot(f"{date}_UITest_top_form.png")
driver.find_element_by_xpath('//*[@id="House_Number"]').send_keys('Gryffindor Halls')
driver.find_element_by_xpath('//*[@id="Street_Name"]').send_keys('Hogwarts School of Witchcraft and Wizardry')
driver.find_element_by_xpath('//*[@id="Town"]').send_keys('Hogsmede')
driver.find_element_by_xpath('//*[@id="County"]').send_keys('Highlands')
driver.find_element_by_xpath('//*[@id="Postcode"]').send_keys('WZ1 1HG')
driver.find_element_by_xpath('//*[@id="Request"]').send_keys('Test')
driver.find_element_by_xpath('//*[@id="Message"]').send_keys('Test message')
driver.save_screenshot(f"{date}_UITest_complete_form.png")
driver.find_element_by_xpath('/html/body/div[4]/div/form/button').click()
time.sleep(10)
driver.save_screenshot(f"{date}_UITest_submit.png")
driver.quit()



