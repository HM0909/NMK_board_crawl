from selenium import webdriver
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
from urllib import request


# 국립중앙박물관(National Museum of Korea)

base_url = "https://www.museum.go.kr"
board_url = base_url + "/site/main/archive/post/category/category_52"

driver = webdriver.Chrome(executable_path='C:\hm_py\chromedriver')
soup = bs(ur.urlopen(board_url).read(), 'html.parser')


# 자료 번호
board_main = soup.find("div",  {"class" : "board-list-tbody"})
board_list = board_main.find_all("ul")

for item in board_list:
    data = item.find("li", {"class":"l"})
    link = data.find("a")
    link_url = link.get("href")                                                         # 상세 URL
    
    driver.get(base_url + link_url)
        
        
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

    
    # print(title.text)
    # print(writer.text)
    # print(reg_date.text)
    # print(read_count.text)
    # print(content.text)
    # print(attach_url)
  
    
# 파일 다운로드
    file_info = detail_soup.find("ul", {"class" : "flie-down-list m-file"})
    file_name = file_info.find("strong").text
    file_url = base_url + attach_url
    
    ext = ".pdf"
    pos = file_name.find(ext)

    savename = "C:/hm_py/board_crawl/" + file_name[:pos]+ext
    request.urlretrieve(file_url, savename)