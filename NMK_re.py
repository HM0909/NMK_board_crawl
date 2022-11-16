from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
import time
from db_manager import DatabaseManager


# 국립중앙박물관(NMK)

base_url = "https://www.museum.go.kr"
board_url = base_url + "/site/main/archive/post/category/category_52" 
login_url = base_url + "/site/main/member/public/login?returnUrl=https%3A%2F%2Fwww.museum.go.kr%2Fsite%2Fmain%2Fhome"

DATABASE_ID = "local"

driver = webdriver.Chrome(executable_path='C:\hm_py\chromedriver')

# 로그인

def login():
    driver.get(login_url)
    
    id = ""
    pwd = ""

    driver.find_element_by_id('id').send_keys(id) 
    time.sleep(5) 
    driver.find_element_by_id('pwd').send_keys(pwd) 
    time.sleep(5) 
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div/div[1]/div[2]/div/a').click() 
    time.sleep(5)
  
  
def crawling():      
    driver.get(board_url)
    
    html = driver.page_source
    soup = bs(html, 'html.parser')
    
    board_main = soup.find("div",  {"class" : "board-list-tbody"}) 
    board_body = board_main.find_all("ul")
   
    datas =[]

    for list in board_body:
        board_list = list.find_all("li")
        board_number = board_list[0].text                                  # 번호
        board_Type = board_list[1].text.strip()                            # 자료 유형
        board_group = board_list[2].text.strip()                           # 구분
        board_wirter = board_list[4].text.strip()                          # 작성자
        
        data = board_list[3]
        link = data.find("a")
        url = link.get("href")                                                         
        link_url = "https://www.museum.go.kr" + url                                   # 상세 URL

        detail(board_number, board_Type, board_group, board_wirter, link_url)
          
        datas.append(detail(board_number, board_Type, board_group, board_wirter, link_url))



    if len(datas) > 0:  
                    db = DatabaseManager(DATABASE_ID)  
                    db.connection()  
                    query = '''  
                            INSERT INTO board_nmk (BD_NUMBER, BD_TYPE, BD_GROUP, LINK_URL, TITLE, WRITER, CONTENT, REG_DATE, READ_COUNT, ATTACH_URL)    
                            VALUES (  
                                %s,
                                %s,   
                                %s,  
                                %s,  
                                %s,  
                                %s,
                                %s,
                                %s, 
                                %s, 
                                %s   
                            )  
                        '''          
                    db.execute_query_bulk(query, datas)



def detail(board_number, board_Type, board_group, board_wirter, link_url):       
    driver.get(link_url)  
         
    detail_html = driver.page_source
    detail_soup = bs(detail_html, 'html.parser')  
 
    detail_main = detail_soup.find("div", {"class" : "board-view-txt"})

    title = detail_main.find("strong", {"class" : "subject"}).text                         # 제목
        
    detail_view = detail_main.find("ul", {"class" : "view-l"})
    view = detail_view.find_all("li")
    
    reg_date_all = view[0].text   
    reg_date = reg_date_all.replace("등록일", "")                                           # 등록일
    read_count_all = view[1].text          
    read_count = read_count_all.replace("조회수", "")                                       # 조회수
    
    content =  detail_main.find("div", {"class" : "pointColor04"}).text                     # 내용
        
    attach_body = detail_main.find("ul",  {"class" : "flie-down-list m-file"})
    attach = attach_body.find_all("li")
    
    attach_url = ""
    
    for list in attach:
        attach_all = list.find("a")
        attach_url= attach_all.get("href")                                                   # 첨부파일 URL                
    
                                                            
    return [board_number, board_Type, board_group, link_url, title, board_wirter, content, reg_date, read_count, attach_url]
  
    
def main(): 

    login()

    crawling()


if __name__ == '__main__':
    main()
