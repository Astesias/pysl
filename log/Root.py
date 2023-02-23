# 2022-12-06 00:45:39  INFO logger.py line12 6
# 2022-12-06 00:45:42  INFO logger.py line12 6
# 2022-12-06 00:45:45  INFO logger.py line12 6

import logging

class elog():
    def __init__(self,filename):
        logging.basicConfig(
                            filename=filename,
                            format='%(asctime)s %(module)s.py line %(lineno)d: %(message)s',
                            datefmt='%Y/%m/%d|%H:%M:%S',
                            level=logging.INFO
                            )
    def add(self,message):
        logging.critical(message)
        
if __name__ == '__main__':
    log=elog('root.txt')
    log.add('sb')