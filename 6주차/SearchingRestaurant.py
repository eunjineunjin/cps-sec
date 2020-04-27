from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

path = os.getcwd() + "/chromedriver.exe"
driver = webdriver.Chrome(path)

try:
    #네이버 지도
    driver.get("https://map.naver.com/v5")
    time.sleep(5)

    searchIndex = "맛집"
    element = driver.find_element_by_class_name("label_search")
    element.send_keys(searchIndex)
    #driver.find_element_by_class_name("btn_search").click()




finally:
    time.sleep(3)
    driver.quit()
