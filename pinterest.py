import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from exceptions import *
from imagehelper import *
from time import sleep
from sys import exit
import asyncio
import os
import pickle

class Pinterest():
    def __init__(self, login, pw):
        self.domains = [".pinterest.com", ".www.pinterest.com", "www.pinterest.com", ".www.pinterest.co.kr", "www.pinterest.co.kr"]
        self.piclist = []
        self.currentdir = os.getcwd()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        if os.path.exists("cookies.pkl"):
            print("Loading cookies...")
            self.driver.get("https://pinterest.com")
            self.driver.implicitly_wait(3)
            sleep(2)
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                # print(cookie)
                for domain in self.domains:
                    try:
                        self.driver.add_cookie({
                            "domain": domain,
                            "name": cookie["name"],
                            "value": cookie["value"],
                            "path": '/'
                            # "expiry": None
                        })
                    except:
                        pass
            self.driver.get("https://pinterest.com")
            self.driver.implicitly_wait(3)
            try:
                self.driver.find_element_by_xpath('//*[@id="HeaderContent"]')
                return
            except:
                print("Failed to login from cookies.. login manually")
                # input()
                # pass
        try:
            self.driver.get("https://pinterest.com/login")
            emailelem = self.driver.find_element_by_id("email")
            passelem = self.driver.find_element_by_id("password")
            emailelem.send_keys(login)
            passelem.send_keys(pw)
            sleep(1)
            self.driver.find_element_by_xpath("//button[@type='submit']").click()
        except Exception as e:
            raise e
        
        while True:
            try:
                self.driver.find_element_by_xpath('//*[@id="HeaderContent"]')
                break
            except:
                sleep(1)
                try:
                    self.driver.find_element_by_xpath("//button[@type='submit']").click()
                except:
                    pass
        self.dump()
        return

    def dump(self):
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl","wb"))

    def crawl(self, dir, scaling, amount):
        timeout = 0
        height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            now_height = self.driver.execute_script("return document.body.scrollHeight")

            # If height changed
            if now_height != height:
                sleep(10)
                self.download_image(scaling, dir, amount)
                break
            else:
                timeout += 1
                if timeout >= 5:
                    print("It seems we find the end of current page, stop crawling.")
                    raise EndPageException
        sleep(2)
        return
    
    def single_download(self, scaling, n=-1, url="https://pinterest.com/", dir="./download", amount=3000):
        global loop
        fail_image = 0
        if n == -1:
            n = 999999999
        loop = asyncio.get_event_loop()

        # Create directory
        if dir[0] == "/":
            dir = dir[1:]
        directory = os.path.join(self.currentdir, dir)
        if not os.path.exists(directory):
            os.mkdir(directory)
        
        self.driver.get(url)
        self.driver.implicitly_wait(3)
        for i in range(n):
            try:
                self.crawl(dir, scaling, amount)
            except EndPageException as e:
                break

            download_pic_count = len(self.piclist)
            print(f"Scroll down {i} Page, downloaded {download_pic_count} images.")

            # End process when maximum amount of images is reached
            if download_pic_count >= amount:
                print(f"{download_pic_count} images were scraped.")
                sys.exit()

        download_pic_count = len(self.piclist)
        print(f"Totally downloaded {download_pic_count} images.")
        loop.close
        return fail_image
    
    def batch_download(self, scaling, n=-1, url_list = [], dir_list = [], dir="./download", amount=3000):
        global loop
        loop = asyncio.get_event_loop()
        url_count = len(url_list)
        dir_count = len(dir_list)
        if n == -1:
            n = 9999999
        if dir_list != [] and url_count != dir_count:
            print("url_list and dir_list must have same length.")
            exit()

        # Open all tabs
        for i in range(url_count-1):
            self.driver.execute_script("window.open('','_blank');")

        for i in range(url_count):
            self.driver.switch_to.window(self.driver.window_handles[i])
            self.driver.get(url_list[i])
            self.driver.implicitly_wait(3)

        for i in range(0,n):
            for uindex in range(url_count):
                dir = dir_list[uindex] if dir_count != 0 else dir

                if dir[0] == "/":
                    dir = dir[1:]
                dir = os.path.join(self.currentdir, dir)
                if not os.path.exists(dir):
                    os.mkdir(dir)
                
                try:
                    self.driver.switch_to.window(self.driver.window_handles[uindex])
                except:
                    continue

                download_pic_count = len(self.piclist)

                try:
                    self.crawl(dir, scaling)
                except EndPageException as e:
                    del url_list[uindex]
                    del dir_list[uindex]
                    self.driver.close()
                    url_count -= 1
                    dir_count -= 1

                print(f"Scroll down from {url_list[uindex]}, {i} Page, downloaded {download_pic_count} images.")

                # End process when maximum amount of images is reached
                if download_pic_count >= amount:
                    print(f"{download_pic_count} images were scraped.")
                    sys.exit()

        return


    def download_image(self, scaling, dir="./download", amount=3000):
        page_pic_list=[]
        req = self.driver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        pins = soup.find_all("div", attrs={"data-grid-item": "true"})

        if pins is None:
            return 0
        for pin in pins:

            # Skip advertisement
            if pin.find(string="Anzeige von") or pin.find(string="Promoted by"):
                print('Skip advertisement')
                continue
            
            img = pin.find('img')

            if img is not None:
                src = img.get("src")
                
                # Profile image, skip
                if "75x75_RS" in src:
                    continue

                if src not in self.piclist:
                    self.piclist.append(src)
                    page_pic_list.append(src)
                
        fail_image = sum(loop.run_until_complete(download_image_host(page_pic_list,dir,scaling)))
        return fail_image
  
    def getdriver(self):
        return self.driver