import requests
from bs4 import BeautifulSoup
import csv

class Scraper():
    def __init__(self):
        self.url = "https://www.billboard.com/charts/billboard-200"

    def getHTML(self):
        res = requests.get(self.url)
        if res.status_code != 200:
            print("request error : ", res.status_code)
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def getCards(self):
        soup = self.getHTML()
        MusicCards = soup.find_all("button", class_ = "chart-element__wrapper")
        self.MusicRank = []
        self.MusicName = []
        self.Artist = []
        self.Trend = []
        LastPeakWeeks = []
        for j in MusicCards:
            self.MusicRank.append(j.find("span", class_ = "chart-element__rank__number").text)
            self.MusicName.append(j.find("span", class_ = "chart-element__information__song").text)
            self.Artist.append(j.find("span", class_ = "chart-element__information__artist").text)
            self.Trend.append(j.find("span", class_ = "chart-element__trend").text)
            LastPeakWeeks.append(j.find("span", class_ = "chart-element__metas").text)

        #LastPeakWeeks 변수를 Last, Peak, Weeks 3개의 변수로 나누기
        self.LastWeek = []
        self.Peak = []
        self.Weeks = []
        LastPeakWeeks2 = []
        for i in range(len(LastPeakWeeks)):
            LastPeakWeeks[i] = LastPeakWeeks[i].replace("\n", " ")
            LastPeakWeeks2.append(LastPeakWeeks[i].split())
            self.LastWeek.append(LastPeakWeeks2[i][0])
            self.Peak.append(LastPeakWeeks2[i][1])
            self.Weeks.append(LastPeakWeeks2[i][2])
        self.writeCSV()

    def writeCSV(self):
        file = open('BillboardChart.csv', 'a', newline = '')
        wr = csv.writer(file)
        for i in range(len(self.MusicRank)):
            Link = "https://www.billboard.com/charts/billboard-200?rank=" + str(i+1)
            wr.writerow([self.MusicRank[i], self.MusicName[i], self.Artist[i], self.Trend[i], self.LastWeek[i], self.Peak[i], self.Weeks[i], Link])
        file.close()

    def scrap(self):
        file = open('BillboardChart.csv', 'w', newline='')
        wr = csv.writer(file)
        wr.writerow(["Rank", "Song", "Artist", "Trend", "Last Week", "Peak", "Weeks", "Link"])
        file.close()
        self.getCards()



if __name__ == "__main__":
    s = Scraper()
    s.scrap()
