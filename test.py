import options as options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options.binary_location = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome" #chrome path
webdriver_path = '/usr/local/bin/chromedriver'
options = Options()
driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

driver.get('https://www.norbelbaby.com.tw/TinTinAppServlet_Test')
username = driver.find_element_by_name('j_username')
username.send_keys('sonic')
userpwd = driver.find_element_by_name('j_password')
userpwd.send_keys('abcd1234')
submit = driver.find_element_by_name('submit')
submit.click()
time.sleep(1)  # Let the user actually see something!

username = driver.find_element_by_name('j_username')
userpwd = driver.find_element_by_name('j_password')
submit = driver.find_element_by_name('submit')
username.send_keys('E11')
userpwd.send_keys('abcd1234')
submit.click()
time.sleep(1)

username = driver.find_element_by_name('j_username')
userpwd = driver.find_element_by_name('j_password')
submit = driver.find_element_by_name('submit')
username.send_keys('maxhsieh')
userpwd.send_keys('00222669max')
submit.click()
time.sleep(1)

driver.quit()
