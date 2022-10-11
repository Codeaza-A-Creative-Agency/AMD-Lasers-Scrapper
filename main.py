import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
class scrap:
    Seller_Platform='AMD-Lasers'
    manufacture='AMD-Lasers'
    manufacture_code='-1'
    titles=[]
    Seller_SKU=[]
    Categories= '-1'
    Sub_Categories='-1'
    Descriptions= []
    Packaging='-1'
    Product_Page_URL=[]
    Image_URL= []
    Att_url=[]
    Attributes='-1'
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

        for p in set(self.p_links):
            
            
            r= requests.get(p)
            bs = BeautifulSoup(r.content, 'lxml')

            variantjson= bs.find('script', id='yoast-schema-graph')
            v_json= json.loads(variantjson.text)
            
            for v_r in v_json['@graph'][5]['offers']:
                imgs=[]
                name= v_r['name']
                self.titles.append(name)
                sku= v_r['sku']
                self.Seller_SKU.append(sku)
                p_link =v_r['url']
                self.Product_Page_URL.append(p_link)
                r= requests.get(p_link)
                bs= BeautifulSoup(r.content,'lxml')
                description= bs.find('div', class_='product-description rte')
                image= bs.findAll('img', class_='FeaturedImage-product-template product-featured-img js-zoom-enabled')
                at_url = bs.find('a', title='Picasso Clario User Manual')
                if at_url !=None:
                    self.Att_url.append(at_url.get('href'))
                else:
                    self.Att_url.append('-1')
                
                for img in image:
                    imgs.append("https:"+img.get('src'))
                self.Image_URL.append(imgs)
                if len(description.text)>2:
                    self.Descriptions.append(description.text)
                if len(description.text)<1:
                    try:
                        descript1= bs.find('p', class_='sc-jWUzzU cKWSZG pf-33_')
                        descript2= bs.find('div', class_='sc-llYSUQ bhKSKZ pf-37_ pf-r pf-r-eh')
                        descript3= bs.find('p', class_='sc-jWUzzU cKWSZG pf-88_')
#                         print('descript1',descript1.text)
#                         print("descript2", descript2.text)
#                         print("descript3",descript3.text)
                        description= ''.join([descript1.text,descript2.text,descript3.text])
                        self.Descriptions.append(description)
#                         print(description)
                    except:
                        pass
            
        

           
    def save_data(self):
        
#         print(len(self.titles))
#         print(len(self.Seller_SKU))
#         print(len(self.Product_Page_URL))
#         print(len(self.Image_URL))
#         print(len(self.Descriptions))
        data_dict={"Seller Platform":self.Seller_Platform, "Seller SKU":self.Seller_SKU, "Manufacture":self.manufacture,"Manufacture Code":self.Seller_SKU,
          "Product Title":self.titles,"Description":self.Descriptions,
         "Packaging":self.Packaging,"Categories":self.Categories,
          "Subcategories":self.Sub_Categories,
           "Product Page URL":self.Product_Page_URL,"Attachment URL":self.Att_url,"Image URL":self.Image_URL, "Attributes":self.Attributes }
        df= pd.DataFrame.from_dict(data_dict)
        df.to_csv("AMD-Lasers-data.csv", index=False)
        
        


    
if __name__ =='__main__':
    scrap=scrap()
    scrap