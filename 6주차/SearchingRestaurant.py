from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

def Crawler(searchIndex):
    path = os.getcwd() + "/chromedriver.exe"
    driver = webdriver.Chrome(path)

    try:
        #멜론에서 가수 검색
        driver.get("https://www.melon.com/")
        time.sleep(3)

        element = driver.find_element_by_xpath('//*[@id="top_search"]')
        element.send_keys(searchIndex)
        driver.find_element_by_xpath('//*[@id="gnb"]/fieldset/button[2]/span').click()

        driver.find_element_by_xpath('//*[@id="conts"]/div[4]/div/div/a').click()

        #전체 페이지 수 찾기
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")
        pages = bs.find("span", class_ = "page_num").find_all("a")[-1].text

        #각 페이지에서 노래 제목 추출
        title = []

        for i in range(int(pages)):
            time.sleep(3)

            html = driver.page_source
            bs = BeautifulSoup(html, "html.parser")

            conts = bs.find("div", id = "pageList").find_all("a", class_ = "fc_gray")

            title.append("page: " + str(i + 1))
            for c in conts:
                title.append(c.text)

            if i != int(pages) - 1:
                driver.find_element_by_xpath('//*[@id="pageObjNavgation"]/div/span/a[' +str(i + 1) + ']').click()

    finally:
        for t in title:
            if t.find("page") != -1:
                print()
                print(t)
            else:
                print(t)

        driver.quit()



if __name__ == "__main__":
    print("가수명을 입력하세요: ")
    Artist = input()
    Crawler(Artist)
