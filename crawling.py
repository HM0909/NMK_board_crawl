import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import logger as logger
from crawl_manager import *
from db_manager import DatabaseManager


PROJECT_NAME = "board_crawl"
RESULT_TEXT_FILE_NAME = "C:/hm_py/board_crawl/result/result_{}.txt"
RESULT_CSV_FILE_NAME = "C:/hm_py/board_crawl/result/result_{}.csv"
HEADER = ['제목', '작성자', '등록일', '조회수', '내용']
ARGV_COUNT = 2
DATABASE_ID = "local"
    

# Create logger
logger = logger.create_logger(PROJECT_NAME)

def create_crawl_manager(board_id):
    # get module from module name
    mod_name = "crawl.{}_crawl".format(board_id)    
    mod = __import__('%s' %(mod_name), fromlist=[mod_name])
    
    # get class in module
    klass = getattr(mod, "{}CrawlManager".format(board_id.capitalize()))
    
    return klass(driver)


# 크롤링
def crawling(manager, board_id):
    urls = []
    results = []

    urls = manager.list()
    
    for url in urls:
        results.append(manager.detail(url))

    datas = []
    
    for result in results:
        result.append(board_id)
        datas.append(result)
        
    db = DatabaseManager(DATABASE_ID)
    db.connection()
    
    query = '''
            INSERT INTO news (TITLE, LINK_URL, WRITER, PUBLISH_DATE, CONTENT, BOARD_ID, REG_DATE)
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

    result = db.execute_query(query, datas)
    
    
def main(args): 
    logger.info("Start crawling...")

    board_id = args[1]

    if board_id != None:
        manager = create_crawl_manager(board_id)

        crawling(manager, board_id)
        
        driver.quit()
    
    logger.info("Finished.")   
    sys.exit(1)

    
# 실행 옵션 설명
def run_info():
    print("Usage: crawling.py [OPTIONS]")
    print("")
    print("Options:")
    print("  --board_id String     [required]")


if __name__ == '__main__':
    for i in range(len(sys.argv)):
        if i > 0:
            logger.info('arg value = %s', sys.argv[i])

    if len(sys.argv) >= ARGV_COUNT:    
        driver = webdriver.Chrome(ChromeDriverManager().install())

        main(sys.argv)
    else:
        logger.error("Requires at least %s argument, but only %s were passed.", ARGV_COUNT-1, len(sys.argv)-1)
        run_info()  