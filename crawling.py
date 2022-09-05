from selenium import webdriver
from bs4 import BeautifulSoup as bs
import urllib.request as ur
import time
from webdriver_manager.chrome import ChromeDriverManager    # Mac
from db_manager import DatabaseManager

HEADER = ['제목', '작성자', '등록일', '내용', '조회수', '첨부파일URL']
ARGV_COUNT = 2
DATABASE_ID = "local"

# 국립중앙박물관(National Museum of Korea)

base_url = "https://www.museum.go.kr"
board_url = base_url + "/site/main/archive/post/category/category_52"
login_url = base_url + "/site/main/member/public/login?returnUrl=https%3A%2F%2Fwww.museum.go.kr%2Fsite%2Fmain%2FexhiSpecialTheme%2Flist%2Fcurrent"

driver = webdriver.Chrome(executable_path='C:\hm_py\chromedriver')    # Windows

def login():
    driver.get(login_url)

    # 로그인
    user_id = ""
    password = ""

    driver.find_element_by_id('id').send_keys(user_id)
    time.sleep(5)
    driver.find_element_by_id('pwd').send_keys(password)
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div/div[1]/div[2]/div/a').click()
    time.sleep(5)


def crawling():
    driver.get(board_url)
    soup = bs(ur.urlopen(board_url).read(), 'html.parser')

    # 자료 번호
    board_main = soup.find("div",  {"class" : "board-list-tbody"})
    board_list = board_main.find_all("ul")

    datas = []
    
    for item in board_list:
        view_writer = item.find_all("li", {"class" : "m-hidden"})
        writer = view_writer[1].text                                                       # 작성자
    
        data = item.find("li", {"class":"l"})
        link = data.find("a")
        link_url = link.get("href")                                                         # 상세 URL

        print(detail(link_url, writer))

        datas.append(detail(link_url, writer))

    if len(datas) > 0:
        db = DatabaseManager(DATABASE_ID)
        db.connection()
        
        query = '''
                INSERT INTO borad (TITLE, LINK_URL, WRITER, PUBLISH_DATE, CONTENT, JOURNAL_ID, REG_DATE)
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    now()
                )                    
            '''        

        db.execute_query(query, datas)

# 상세 크롤링
def detail(detail_url, writer):
    driver.get(base_url + detail_url)

    detail_html = driver.page_source 
    detail_soup = bs(detail_html, 'html.parser')

    view_header = detail_soup.find("div", {"class" : "view-header"})
    title = view_header.find("strong", {"class" : "subject"})                           # 제목
    
    view_header_li_list = view_header.find_all("li")

    reg_date_all = view_header_li_list[0]                                                   # 등록일
    reg_date = reg_date_all.text.replace("등록일", "")
    
    read_count_all = view_header_li_list[1]                                                 # 조회수
    read_count = read_count_all.text.replace("조회수", "")
    
    content = detail_soup.find("div", {"class" : "pointColor04"})                       # 내용
    
    attach = detail_soup.find("a", {"class" : "btn btn-m-line bk2 btn-file-down"})
    attach_url = attach.get("href")                                                            # 첨부파일 URL
            
    return [title.text, writer.strip(), content.text, detail_url, reg_date, read_count, attach_url] 


def main(): 
    # driver.get(base_url)
    login()
    
    crawling()
    
    driver.quit()
    
if __name__ == '__main__':
    main()
