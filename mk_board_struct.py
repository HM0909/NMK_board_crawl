from selenium import webdriver
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
from urllib import request
from crawl_manager import *


# 국립중앙박물관(National Museum of Korea)

BASE_URL = "https://www.museum.go.kr"
BOARD_URL = BASE_URL + "/site/main/archive/post/category/category_52"
LOGIN_URL = BASE_URL + "/site/main/member/public/login?"

driver = webdriver.Chrome(executable_path='C:\hm_py\chromedriver')
driver.get(LOGIN_URL)


# 로그인
user_id = "haemin9299"
password = "@lhmlove1524"


driver.find_element_by_id('id').send_keys(user_id)
time.sleep(5)
driver.find_element_by_id('pwd').send_keys(password)
time.sleep(5)
driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div/div[1]/div[2]/div/a').click()
time.sleep(5)

driver.get(BOARD_URL)

soup = bs(ur.urlopen(BOARD_URL).read(), 'html.parser')


class ChosunCrawlManager(CrawlManager):
    def __init__(self, driver):
        self.driver = driver


    def list(self):     
        self.driver.get(BASE_URL)
        
        # 자료 번호
        board_main = soup.find("div",  {"class" : "board-list-tbody"})
        board_list = board_main.find_all("ul")

        for item in board_list:
            data = item.find("li", {"class":"l"})
            link = data.find("a")
            link_url = link.get("href")                                                         # 상세 URL
            
            driver.get(BASE_URL + link_url)


    def detail(self, url):
        detail_html = url
                
        # 세부사항
        detail_html = driver.page_source 
        detail_soup = bs(detail_html, 'html.parser')

        view_header = detail_soup.find("div", {"class" : "view-header"})
        title = view_header.find("strong", {"class" : "subject"})                           # 제목
        
        view_writer = item.find_all("li", {"class" : "m-hidden"})
        writer = view_writer[1]                                                             # 작성자

        view_header_li_list = view_header.find_all("li")
        reg_date = view_header_li_list[0]                                                   # 등록일
        read_count = view_header_li_list[1]                                                 # 조회수
        
        content = detail_soup.find("div", {"class" : "pointColor04"})                       # 내용
        
        attach = detail_soup.find("a", {"class" : "btn btn-m-line bk2 btn-file-down"})
        attach_url = attach.get("href")                                                     # 첨부파일 URL

        
        return [title, detail_html, writer, reg_date, content]


        # print(title.text)
        # print(writer.text)
        # print(reg_date.text)
        # print(read_count.text)
        # print(content.text)
        # print(attach_url)
        
            
        # # 파일 다운로드
        #     file_info = detail_soup.find("ul", {"class" : "flie-down-list m-file"})
        #     file_name = file_info.find("strong").text
        #     file_url = BASE_URL + attach_url
            
        #     ext = ".pdf"
        #     pos = file_name.find(ext)

        #     savename = "C:/hm_py/board_crawl/" + file_name[:pos]+ext
        #     request.urlretrieve(file_url, savename)