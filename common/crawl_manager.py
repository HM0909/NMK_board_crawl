import os
import logging
# import utils.file_util as file

from abc import *
from urllib.request import urlopen

class CrawlManager(metaclass=ABCMeta):
    driver = None
    logger = logging.getLogger()
    
    # 회원 데이터 수집
    @abstractmethod
    def list(self):
        pass
    
    
    # 게시물 수집
    @abstractmethod
    def detail(self, url):
        pass