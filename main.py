from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
option = Options()
option.add_argument("--headless")
driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()), options=option)
class scrap:
    titles=[]
    skus=[]
    descripts= []
    images= []
    p_url=[]
    links=[]
    p_links=[]
    def __init__(self):
        self.parse()
        self.save_data()
        
    def parse(self):
        url = 'https://www.amdlasers.com'
        r= requests.get(url)
        bs=BeautifulSoup(r.content,'lxml')
        divs= bs.findAll('a',class_='site-nav lvl-1')
        for i in divs:
            link= url+i.get('href')
            if 'products/' in link:
                self.p_links.append(link)
                pass
            if 'collections/' in link:
                self.links.append(link)
        #         print("Collections",link)

        for req in self.links:
            r= requests.get(req)
            divs=bs.findAll('a', class_='grid-view-item__link')
            for i in divs:
                self.p_links.append(url+i.get('href'))

        for p in self.p_links:
            imgs=[]
            driver.get(p)
#             print(p)
            title= driver.find_element(By.XPATH,"//h1[@class='product-single__title']")
            sku= driver.find_element(By.XPATH,'//span[@class="variant-sku"]')
            description=driver.find_element(By.XPATH,"//div[@class='product-description rte']")
            image= driver.find_elements(By.XPATH,"//img[@class='FeaturedImage-product-template product-featured-img js-zoom-enabled']")
            self.titles.append(title.text)
            self.skus.append(sku.text)
            self.p_url.append(p)
            for img in image:
                imgs.append(img.get_attribute('src'))

            self.images.append(imgs)
            try:
                self.descripts.append(description.text)
            except:
                self.descripts.append("No description available")
    def save_data(self):
        data_dict={"Title":self.titles, "Seller SKU": self.skus, "Description":self.descripts, "Image URL": self.images, "Product Page URL":self.p_url}
        df= pd.DataFrame.from_dict(data_dict)
        df.drop_duplicates()
        df.to_csv("AMDlasers.csv", index=False)

if __name__ =='__main__':
    scrap=scrap()