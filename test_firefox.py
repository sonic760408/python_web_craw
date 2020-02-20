from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

firefox_path = "/Applications/Firefox.app/Contents/MacOS/firefox" #firefox path
webdriver_path = '/usr/local/Cellar/geckodriver/0.26.0/bin/geckodriver'
binary = FirefoxBinary(firefox_path)
driver = webdriver.Firefox(executable_path=webdriver_path,firefox_binary=binary) #開啟firefox
driver.get("https://freelancerlife.info/") #前往這個網址
time.sleep(2)
driver.close()