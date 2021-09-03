import pickle
from selenium import webdriver
import json
import time 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
import pyautogui


#------------------------------------------------------------------------------------------------------------------------------------------------
#webdriver firefox with profile


myprofile = webdriver.FirefoxProfile(r'C:\Users\crysi\AppData\Roaming\Mozilla\Firefox\Profiles\m871l255.default-release')

driver = webdriver.Firefox(firefox_profile=myprofile,executable_path=r"C:\Users\crysi\Desktop\geckodriver.exe")
#firefox_profile=myprofile,


#------------------------------------------------------------------------------------------------------------------------------------------------
#zabbix loading and adding cookies


driver.get("https://zabbix.bobbie.de/zabbix.php?action=dashboard.view")

cookies = pickle.load(open("D:\Bobbie2.0\BobbieDashboard2.0-ScriptFirefox\cookiesZab.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()


#------------------------------------------------------------------------------------------------------------------------------------------------
#hubspot loading and adding cookies


driver.get("https://app.hubspot.com/reports-dashboard/9232473/view/8219673")

cookies = pickle.load(open("D:\Bobbie2.0\BobbieDashboard2.0-ScriptFirefox\cookiesHs.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()


#------------------------------------------------------------------------------------------------------------------------------------------------
#connect to dashboard

driver.get("http://127.0.0.1:8050/")


#------------------------------------------------------------------------------------------------------------------------------------------------
#make fullscreen

pyautogui.press('f11')


#------------------------------------------------------------------------------------------------------------------------------------------------
