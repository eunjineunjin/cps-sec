from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

path = os.getcwd() + "/chromedriver.exe"
driver = webdriver.Chrome(path)

try:
    #교보문고 메인 페이지에서 파이썬 검색
    driver.get("http://www.kyobobook.co.kr/index.laf?OV_REFFER=https://www.google.com/")
    time.sleep(1)

    searchIndex = "파이썬"
    element = driver.find_element_by_class_name("main_input")
    element.send_keys(searchIndex)
    driver.find_element_by_class_name("btn_search").click()


    #파이썬 검색 화면에서 전체 페이지 수 찾기
    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")

    pages = bs.find("span", id = "totalpage").text

    print(pages)


    #각 페이지에서 정보 추출
    title = []

    for i in range(3):
        time.sleep(5)

        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        conts = bs.find("div", class_ = "list_search_result").find_all("td", class_ = "detail")

        title.append("page" + str(i + 1))
        for c in conts:
            title.append(c.find("div", class_ = "title").find("strong").text)

        #다음 페이지
        driver.find_element_by_xpath('//*[@id="contents_section"]/div[9]/div[1]/a[3]').click()


finally:
    for t in title:
        if t.find("page") != -1:
            print()
            print(t)
        else:
            print(t)

    driver.quit()
