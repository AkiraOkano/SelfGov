''' 
Created on 2025/03/26

@author: Akira Okano
'''
import datetime;
import logging
from logging import getLogger, StreamHandler, Formatter, FileHandler
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import traceback

logger = getLogger("SelfGov")

def processURL(url, driver):
    #logger.info(url)

    try:
        driver.get(url)
    except:
        logger.error("driver time out")
        print("driver time out")
        return "", ""
    #WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'skin-pagingNext')))
    html = driver.page_source.encode('utf-8')
    #result = requests.get(url)
    #c = result.content
    soup = BeautifulSoup(html,'lxml')
    allCount=soup.find("span",{'id':'cpd_number_getreadsall'})
    count=soup.find("span",{'id':'cpd_number_getreadsthismonth'})
    #print(allCount.getText())
    #print(count.getText())
    
    return allCount, count 

def setLogger():
    formatter = '%(levelname)s : %(asctime)s : %(message)s'
    #logging.basicConfig(filename='ameblo.log', level=logging.DEBUG, format=formatter)
    logger = logging.getLogger(__name__)

    logger.setLevel(logging.INFO)

    stream_handler = StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(handler_format)
    logger.addHandler(stream_handler)
    file_handler = FileHandler('SelfGov.log', 'a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(handler_format)
    logger.addHandler(file_handler)
    logger.info('start')
    return logger

if __name__ == '__main__':
    try:
        logger=setLogger();
        now = datetime.datetime.now();
        year=now.year;
        month=now.month;
        date=now.day;
        hour=now.hour;
        minute=now.minute;
    
        today = now.strftime("%Y/%m/%d") 
    # datetime.date.today()
        time = now.strftime("%H:%M")
    
        url= "https://www.higashirinkan.org/"
    #columns = ["year","month","day","hour","minute","total","thismonth"]
        columns = ["date","time","total","thismonth"]
        df = pd.DataFrame(columns=columns)
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        filename = "SelfGov.csv"
        allCount, count=processURL(url, driver)
        driver.quit()
        logger.info(allCount.getText())
        logger.info(count.getText())
        se = pd.Series([today, time, allCount.get_text(), count.getText()], columns)
        df=pd.DataFrame([se])
        df.to_csv(filename, encoding = 'utf-8-sig', mode='a', header=False, index=False)
    except Exception as e:
        etype, value, tb = sys.exc_info()
        logger.error(traceback.format_exception(etype, value, tb))
        sys.exit(1)
    logger.info("end")



