# import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


url = "https://serviceexpress.com/resources/eol-eosl-database/"

class ExpressScrapper:
    def __init__(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))

    def open_url(self, url):
        self.driver.get(url)
        # time.sleep(5)

    def get_product_urls(self):
        no_of_products = self.driver.find_elements(By.XPATH, "/html/body/main/div[2]/article/div/div/div[2]/div[3]/ul/li")
        product_list = []
        for i in range(1, len(no_of_products)):
            xpath = "/html/body/main/div[2]/article/div/div/div[2]/div[3]/ul/li["+str(i)+"]/a"
            product_list.append(self.driver.find_element(By.XPATH, xpath).get_attribute("href"))
        return product_list

    def save_to_file(self, data):
        with open("data.txt","a") as f:
            for d in data:
                f.write(d+", ")
            f.write("\n")
            f.close()

    def get_pages(self):
        def get_no_of_pages(url):
            no_of_pages = 0
            if no_of_pages == 0:
                self.open_url(url)
                no_of_pages = self.driver.find_element(By.XPATH, "/html/body/main/div[2]/section/nav/div/span[2]/span").text
            return no_of_pages

        product_urls = self.get_product_urls()
        for product in product_urls:
            no_of_pages = get_no_of_pages(product)
            if no_of_pages != 0:
                for i in range(1,int(no_of_pages)):
                # for i in range(1, 2):
                    self.open_url(product+"/page/"+str(i))
                    required_links = []
                    no_of_req_links = self.driver.find_elements(By.CLASS_NAME,"content-card")
                    for i in range(1, len(no_of_req_links)):
                    # for i in range(1, 2):
                        l = []
                        link = self.driver.find_element(By.XPATH, "//*[@id='main']/div[2]/section/div/article["+str(i)+"]/div/div[2]/header/h2/a").get_attribute('href')
                        required_links.append(link)
                        self.driver.execute_script("window.open('');")
                        self.driver.switch_to.window(self.driver.window_handles[1])
                        self.driver.get(link)
                        for i in range(1,7):
                            l.append(self.driver.find_element(By.XPATH, "/html/body/main/article/div/div/div/div[1]/dl/div["+str(i)+"]/dd").text)
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        self.save_to_file(l)
            

scrapper = ExpressScrapper()
scrapper.open_url(url)
scrapper.get_pages()
