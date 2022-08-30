# reference : https://github.com/hyunji-Hong/Crawling_Paper

'''
OS       : MacOS(Monterey 12.5)
Python   : 3.10.6
Selenium : 2.33.0
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium
from time import sleep
import pickle

"""GLOBALS"""
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'      # Path of the chrome-drive 
driver = webdriver.Chrome(CHROMEDRIVER_PATH)

def getAdvisoryInfo(selector) :
    advisoryInfos = []
    
    try :
        #go into each advisory page
        advisoryPage = driver.find_element(By.CSS_SELECTOR, selector); 
        # advisoryPage = driver.find_element_by_css_selector(selector)
        advisoryPage.click()
    except Exception :
        sleep(1)
        print("게시물들어가다가 에러발생")
        getAdvisoryInfo(selector)

    #wait loading...
    sleep(1.5)
    try: 
        advisoryInfos = crawl()
    except Exception :
        sleep(1)
        print("여기선 에러 안나겠지만 크롤링불러올때")
        advisoryInfos = crawl() 
    driver.back()

    return advisoryInfos

def crawl() : 
    try : 
        #crawl GHSA code
        ghsa = driver.find_element(By.CSS_SELECTOR,'div.col-12.col-md-3.float-left.pt-3.pt-md-0 > div:nth-child(4) > div').text
        
        #crawl package info
        packages = driver.find_elements(By.CSS_SELECTOR,'div.Box-body span.f4.color-fg-default.text-bold')
        package = [info.text for info in packages]

        # crawl affected Version info
        affectedVers = driver.find_elements(By.XPATH,'//*[@id="js-pjax-container"]/div/div[2]/div[1]/div[1]/div/div/div[2]/div')
        affectedVer = [info.text for info in affectedVers]

        # crawl patched Version info
        patchedVers = driver.find_elements(By.XPATH,'//*[@id="js-pjax-container"]/div/div[2]/div[1]/div[1]/div/div/div[3]/div')
        patchedVer = [info.text for info in patchedVers]
    except Exception :
        print("크롤링하다가 에러 발생")
        sleep(1)
        crawl()


    advisoryInfo = [ghsa, package, affectedVer, patchedVer]
    return advisoryInfo

def main() :
    try :
        #open GitHub Advisory Database
        advisoryDB = {}
        url = 'https://github.com/advisories?query=type%3Areviewed'
        driver.get(url)

        #get TotalPage count
        max = 25
        total = int(driver.find_element(By.CSS_SELECTOR,'div.Box-header.d-flex > h2 > span').text.replace(",",""))
        # total = int(driver.find_element_by_css_selector('div.Box-header.d-flex > h2 > span').text.replace(",",""))
        page, lastpage = divmod(total, max)
        page += 1

        for i in range(1,page+1) :
            if i == page : max = lastpage
            for j in range(max) : 
                selector = 'div.Box.Box--responsive.js-navigation-container.js-active-navigation-container > div:nth-child('+str(j+2)+') > div > div > div > a'
                advisoryInfo = getAdvisoryInfo(selector)
                print(advisoryInfo)
                advisoryDB[advisoryInfo.pop(0)] = advisoryInfo #{GHSA : [package, affected, patched]}

                #save in file
                with open('/Users/kiara/Desktop/AdvisoryDUMP.txt','a') as f :
                    for key, value in advisoryDB.items() :
                        dump = str(key)+" : "+str(value)
                        f.write(dump+"\n")

            # gotoNextpage()  
            driver.get(f'https://github.com/advisories?page={i+1}')
    except Exception :
        print("메인에서 에러발생")

    finally :
        #save as dictionary dataset
        with open("/Users/kiara/Desktop/Advisory_DB.txt", 'wb') as f:
            pickle.dump(advisoryDB, f)
        driver.close()

""" EXECUTE """
if __name__ == "__main__":
    main()


    '''
######################################################################################################
개선하면 좋을 문제들
    1. patchedVers의 CSS 앨리먼트가 affectedVers와 중첩(포함관계)되서 patchedVers에 affectedVers가 들어가는 문제.
        - 현재로는 patchedVers 크롤링한뒤 홀수 번째만 필터링하여 사용중
            * '22.08.30 해결: CSS Selector -> XPath 으로 변경
    2. 각 advisory페이지에 진입 -> 크롤링 -> 빠져나옴 을해서 부하가 많이 걸리는듯함.
    3. 페이지 로딩때문에 sleep() 사용 중. 스레드로 더 빠르게할수 있을까?
    3. selenium 4.0 버전 호환가능하도록 재작성필요
        * '22.08.30 해결: 4.0.0 버전 & 그 미만 버전으로 분화
 
#######################################################################################################   '''