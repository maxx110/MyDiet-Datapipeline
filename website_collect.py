from cgitb import text
import os
from sys import implementation
from this import d
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import uuid
import json
import urllib.request


class scrapper:
    def __init__(self):
        self.driver =webdriver.Edge()
        self.url = 'https://www.myprotein.com/'
        self.data = {'Unique_Id': [], 'Product_Id': [], 'Product_Name': [], 'Product_Price': [], \
        'Product_Link': [], 'Product_img': [],'Product_description': []}
        self.img = []
        
        #self.uid = uuid.uuid4()


    def open_website(self):
        self.driver.get(self.url)

    def accept_cookies(self):
        try:            
            accept_cook= self.driver.find_element(By.XPATH,'//*[@id="home"]/div[4]/div/div[2]/button')
            accept_cook.click()
            accept_cookies= self.driver.find_element(By.XPATH,"//*[@id='home']/div[1]/div/div/div[2]/button")
            accept_cookies.click()
        except:
            print('something is wrong')

    def click_on_vitamins(self):
        locate_vitamins = self.driver.find_element(By.XPATH,"//main[@id='mainContent']//a[4]")
        click_on_vitamins =locate_vitamins.click()

    def scroll_down_to_last_page(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)

    def click_on_view_all(self):
        locate_view_all = self.driver.find_element(By.XPATH,"//a[normalize-space()='View all']")
        click_on_view_all = locate_view_all.click()

    # def download_image(self):
    #     path1 = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data'
    #     os.chdir(path1)
        
    #     if not os.path.exists(path):
    #         os.makedirs('images') 
    #     else:
    #         pass
    #     path_2 = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images'
    #     os.chdir(path_2)
    #     for i in self.img:
    #         urllib.request.urlretrieve(i, path_2 + '\\' + .jpg)

    def download_img(self):
        #path3 = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data'
        #os.chdir(path3)
        path3 = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images'
        
        # if not os.path.exists(path3):
        #     os.makedirs(path3) 
        # else:
        #     pass

        # path4 = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images'
        # os.chdir(path4)
        # for i in self.img:
        #     #lnum = len(self.img)
        #     #filename = i.split('-'[-1])
        #     urllib.request.urlretrieve(i,f'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images\\a.jpg')

       
        all_product = self.driver.find_elements(by=By.XPATH, value="//li[contains(@class,'productListProducts_product')]")
        for i in all_product:
            if not os.path.exists(path3):
                os.makedirs(path3) 
            img = i.find_element(By.XPATH, "//div[@class='athenaProductBlock_imageContainer']")
            a_tag = img.find_elements(By.TAG_NAME,'img')
            print(a_tag)
            for i in a_tag:
                prd_img= i.get_attribute('src')
                print(prd_img)
                #img_name = prd_img.split('/'[-1])
                urllib.request.urlretrieve(prd_img, f'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images\\a.jpg')

    
        

        
        

    def get_all_product(self):
        
        
        all_product = self.driver.find_elements(by=By.XPATH, value="(//li[contains(@class,'productListProducts_product')])")
        
        for products in all_product:
           
            
            #gets the product title and return only the text
            product_title= products.find_element(By.XPATH, ".//h3[@class='athenaProductBlock_productName']").text
            
            #gets the product price but it checks for the xpath for both
            """
            try:
                product_price = products.find_element(By.XPATH,".//span[@class='athenaProductBlock_fromValue']").text
            except:
                product_price = products.find_element(By.XPATH,".//span[@class='athenaProductBlock_priceValue']").text
            """
            #gets the product links
            link = products.find_element(By.XPATH, ".//div[@class='athenaProductBlock']")
            a_tag = link.find_element(By.TAG_NAME,'a')
            product_link = a_tag.get_attribute('href')

            #get product unique id
            unik = products.find_element(By.XPATH, ".//div[@class='athenaProductBlock_title']")
            a_tag = unik.find_element(By.TAG_NAME,'h3')
            product_unikk = a_tag.get_attribute('id').split('-')
            product_unik = product_unikk[1]
            
            #Generate a uui unique global id for each record
            UniqueIds = uuid.uuid4()
            UniqueId = str(UniqueIds) 

            #gets the product image
            img = products.find_element(By.XPATH, ".//div[@class='athenaProductBlock_imageContainer']")
            a_tag = img.find_element(By.TAG_NAME,'img')
            product_img = a_tag.get_attribute('src')
            
            #gets the product description
            try:
                product_text= products.find_element(By.XPATH, ".//span[@class='papBanner_text']").text           
            except:
                pass
            
            raw_datas = {'Unique_Id': [], 'Product_Id': [], 'Product_Name': [], 'Product_Price': [], \
            'Product_Link': [], 'Product_img': [],'Product_description': []}

            # APPEND VARIOUS RETRIEVAL TO ITS RESPECTIVE DICTIONARY
            self.data['Unique_Id'].append(UniqueId)
            self.data['Product_Id'].append(product_unik)
            self.data['Product_Name'].append(product_title)
            #self.data['Product_Price'].append(product_price)
            self.data['Product_Link'].append(product_link)
            self.data['Product_img'].append(product_img)
            self.data['Product_description'].append(product_text)

            raw_datas['Unique_Id'].append(UniqueId)
            raw_datas['Product_Id'].append(product_unik)
            raw_datas['Product_Name'].append(product_title)
            #raw_datas['Product_Price'].append(product_price)
            raw_datas['Product_Link'].append(product_link)
            raw_datas['Product_img'].append(product_img)
            raw_datas['Product_description'].append(product_text)

            
            self.img.append(product_img)

            path1 = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data'
           
            os.chdir(path1)
            os.mkdir(product_unik)
            
            path2 = f'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\{product_unik}'
            os.chdir(path2)
            
            with open('data.json', 'a') as f:
                json.dump(raw_datas, f)

            raw_datas.clear()

   
        
            
            

            
           
            

            

            

    def test(self):
        self.open_website()
        #self.driver.maximize_window()
        self.driver.implicitly_wait(20)
        self.accept_cookies()
        self.driver.implicitly_wait(20)
        self.click_on_vitamins()
        self.click_on_view_all()
        self.scroll_down_to_last_page()
        self.driver.implicitly_wait(20)
        sleep(5)
        #self.get_all_product()
        #sleep(5)
        #self.driver.close()
        #print(self.data)
        #print(self.img)
        #self.download_image()
        self.download_img()





if __name__ == '__main__':
    path = 'raw_data'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        pass
    data=scrapper()
    data.test()    


