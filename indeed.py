import requests
from bs4 import BeautifulSoup
import csv

class Scraper():
    def __init__(self):
        self.url = "http://kr.indeed.com/jobs?q=python&limit=50"
        self.cnt = 0

    def getHTML(self):
        res = requests.get(self.url + "&start=" + str(self.cnt*50))
        if res.status_code != 200:
            print("request error : ", res.status_code)
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def getPages(self, soup):
        pages = soup.select(".pagination > a")
        return len(pages)

    def getCards(self, soup):
        jobCards = soup.find_all("div", class_ = "jobsearch-SerpJobCard")
        jobID = []
        jobTitle = []
        jobLocation = []
        for j in jobCards:
            jobTitle.append(j.find("a").text.replace("\n", ""))
            if j.find("div", class_ = "location") != None:
                jobLocation.append(j.find("div", class_ = "location").text)
            elif j.find("span", class_ = "location") != None:
                jobLocation.append(j.find("span", class_ = "location").text)
            jobID.append("http://kr.indeed.com/viewjob?jk=" + j["data-jk"])
        self.writeCSV(jobID, jobTitle, jobLocation)

    def writeCSV(self, ID, Title, Location):
        file = open('indeed.csv','a', newline='')
        wr = csv.writer(file)
        for i in range(len(ID)):
            wr.writerow([str(i+1+self.cnt*50), ID[i], Title[i], Location[i]])
        file.close()
        self.cnt = self.cnt + 1

    def scrap(self):
        soupPage = self.getHTML(0)
        pages = self.getPages(soupPage)
        file = open('indeed.csv', 'w', newline='')
        wr = csv.writer(file)
        wr.writerow(["No.", "Link","Title", "Location"])
        file.close()

        for i in range(pages) :
            soupCard = self.getHTML()
            self.getCards(soupCard)



if __name__ == "__main__":
    s = Scraper()
    s.scrap()
