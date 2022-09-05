import os
import sys
import yaml
import pymysql
import logging

class DatabaseManager:
    conn = None
    logger = logging.getLogger()
    
    def __init__(self, database_id):
        self.database_id = database_id

    
    def datasource(self):           
        try:
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),"."))
            doc = yaml.load(open(os.path.join(root_dir, 'config', 'datasource.yml'), 'r'), Loader=yaml.SafeLoader)
            return doc[self.database_id]
        except IOError as e:
            self.logger.error(e)
            sys.exit(1)


    def connection(self):
        datasource = self.datasource()

        try:
            self.conn = pymysql.connect(host=datasource['host'], port=datasource['port'], 
                                        user=datasource['username'], passwd=datasource['password'], 
                                        db=datasource['database'],charset='utf8',autocommit=False)
            self.logger.info("Connected to %s ." % datasource['host'])
        except Exception as e:
            self.logger.error("Failed connect to %s ." % datasource['host'])
            self.logger.error(e)


    def close(self):
        if self.conn != None:
            self.conn.close()    


    def execute_query(self, query, value):
        cs = self.conn.cursor()
        result = 0
        
        try:
            cs.execute(query, value)
            self.conn.commit()
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()
            result = -1
        finally:
            cs.close()
            return result


    def execute_query_bulk(self, query, value):
        cs = self.conn.cursor()
        result = 0
        
        try:
            cs.executemany(query, value)
            self.conn.commit()
        except Exception as e:
            self.logger.error(e)
            self.conn.rollback()
            result = -1
        finally:
            cs.close()
            return result


    def select_query(self, query):
        cs = self.conn.cursor()
        
        try:
            cs.execute(query)
            return cs.fetchall()
        except Exception as e:
            self.logger.error(e)
        finally:
            cs.close()


    def select_query_as_dicts(self, query):
        cs = self.conn.cursor()
            
        try:
            cs.execute(query)
            columns = [i[0] for i in cs.description]
            return [dict(zip(columns, row)) for row in cs.fetchall()]
        except Exception as e:
            self.logger.error(e)
        finally:
            cs.close()