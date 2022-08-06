from selenium import webdriver
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import time
import csv
from urllib import request

# 국립중앙박물관(National Museum of Korea)

base_url = "https://www.museum.go.kr/site/main/archive/post/category/category_52"
login_url = "https://www.museum.go.kr/site/main/member/public/login?returnUrl=https%3A%2F%2Fwww.museum.go.kr%2Fsite%2Fmain%2FexhiSpecialTheme%2Flist%2Fcurrent"

driver = webdriver.Chrome(executable_path='C:\hm_py\chromedriver')
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

driver.get(base_url)