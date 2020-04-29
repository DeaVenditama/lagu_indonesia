from selenium import webdriver
from bs4 import BeautifulSoup
from database import Database

class Scrape:
    def __init__(self):
        chromeOptions = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images':2}
        chromeOptions.add_experimental_option("prefs", prefs)
        #chromeOptions.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        self.url_home = "https://lirik.kapanlagi.com/lagu/"

    def getSongList(self, abjad):
        i=1
        self.driver.get(self.url_home+""+abjad+"_id/index"+str(i)+".html")
        db = Database()
        column = ('judul', 'penyanyi','link','lirik') 
        while True:
            try:
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                songList = soup.find_all('div', attrs={'class':'div-horizontal2-list'})
                data_insert = []
                for song in songList:
                    a = song.find('a')
                    link = a.get('href')
                    judul = a.get_text()
                    penyanyi = song.find('span').get_text()
                    lirik = self.getSongLyric(link)
                    print("Judul: "+judul)
                    print("Link: "+link)
                    print("Penyanyi: "+penyanyi)
                    print("Lirik: "+lirik)
                    rowData = (judul, penyanyi, link, lirik)
                    data_insert.append(rowData)
                insert = db.insert_into("lagu", column, data_insert)
                i = i+1
                self.driver.get(self.url_home+""+abjad+"_id/index"+str(i)+".html")
                print("=============================")
                print("CHANGE TO NEXT PAGE")
                print("=============================")
                if insert != True:
                    break
            except Exception as err:
                print("==================ERROR===============")
                print(err)
                print("==================ERROR===============")
                break 

    def getSongLyric(self, link):
        self.driver.get(link)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        lyricBody = soup.find_all('span', attrs={'class':'lirik_line'})
        lyricText = []
        for lyric in lyricBody:
            lyricText.append(lyric.get_text())
        return "\n".join(lyricText)

    def crawl(self):
        #abjad = "a bc d e f g h i j k l m n o p q r s t u v w x y num"
        #abjad_list = abjad.split()
        #for word in abjad_list:
        #    self.getSongList(word)
        self.getSongList('num')
        self.driver.quit()

scrape = Scrape().crawl()

        
