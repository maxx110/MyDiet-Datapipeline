from cgitb import text
import os
from this import d
from time import sleep, time
from tkinter import image_names
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.chrome.options import Options
#from msedge.selenium_tools import EdgeOptions
import uuid
import json
import urllib.request
import boto3
import glob
import connection
import psycopg2
import psycopg2.extras as extras
import pandas as pd
from connection import Migration
from s3_function import s3_functions
#from die import send






class scrapper(Migration):

    def __init__(self):
        super().__init__()
        COptions = Options()
        COptions.use_chromium = True
        COptions.add_argument("--headless")
        COptions.add_argument("--disable-gpu")
        COptions.add_argument("--disable-dev-shm-usage")
        COptions.add_argument("--no-sandbox")
        COptions.add_argument('--allow-running-insecure-content')
        COptions.add_argument('--ignore-certificate-errors')
        #COptions.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.driver =webdriver.Chrome(chrome_options=COptions)
        self.url = 'https://www.myprotein.com/'
        self.data = {'Unique_Id': [], 'Product_Id': [], 'Product_Name': [], 'Product_Price': [], \
        'Product_Link': [], 'Product_img': [],'Product_description': []}
        self.img = []
        self.rescrape_tag = False
        
        
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
        locate_vitamins = self.driver.find_element(By.XPATH,"//*[@id='mainContent']/div[2]/a[4]")
        locate_vitamins.click()

    def scroll_down_to_last_page(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)

    def click_on_view_all(self):
        locate_view_all = self.driver.find_element(By.XPATH,"//a[normalize-space()='View all']")
        locate_view_all.click()

    
    def convert_to_dataframe(self):
        # df = pd.DataFrame.from_dict(self.data, orient='index')
        # data_frame = df.transpose()
        super().con_database()  #establish connecction to databse
        super().create_schema() #creates a schema for database
        super().create_table()  #creates a table if not exists
    #   super().est_conn(data_frame) #loads dataframe to postgres database

    def dump_raw_data_to_s3(self,raw_datas,product_unik):
        # dump each as a json file into an s3 bucket
        bucket_name = 'aicorbuc'
        s3 = boto3.client('s3')
        data = json.dumps(raw_datas)
        s3.put_object(Body=json.dumps(data),Bucket=bucket_name,Key= f'website_data/{product_unik}')



    def uploadDirectory(self):
        """
        upload the downloaded image into the required s3_bucket 
        """
        try:
            s3= boto3.client('s3')
            bucket_name = 'aicorbuc'
            files_in_image_folder = glob.glob('C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images\\*')
            
            for file in files_in_image_folder:
                file_name = file.split('-')[-1]
                s3.upload_file(file,bucket_name,f'website_data/images/{file_name}')
        except:
            print('image upload to s3 failed')

    def avoid_rescrap(self,prd_unik):    
        raw_folder_path = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data'
        for root_folder,sub_folder,files in os.walk(raw_folder_path):
            for file in files:
                if file == prd_unik:
                    self.rescrape_tag = True
                    break
                else:
                    pass
        return self.rescrape_tag
                
                

       

 
    def download_img(self):
        """
        download the image from the src from the web
        """
        image_path = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images'    
        #make a folder to the image path
        make_folder(image_path)
        

        #get all images
        product_lists = self.driver.find_elements(by=By.XPATH, value="//li[contains(@class,'productListProducts_product')]")
        bucket_name = 'aicorbuc'
        s3 = boto3.client('s3')
        answer = input('Do you want to upload to s3: Yes/No')
        try:
            for product in product_lists:
                
                if not os.path.exists(image_path):
                    os.makedirs(image_path) 
                img = product.find_element(By.XPATH, ".//div[@class='athenaProductBlock_imageContainer']")
                a_tags = img.find_elements(By.TAG_NAME,'img')
                #print(a_tag)
                for each_a_tag in a_tags:
                    prd_img= each_a_tag.get_attribute('src')
                    #print(prd_img)
                    img_name = prd_img.split('/')[-1]
                    try:
                        urllib.request.urlretrieve(prd_img, f'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images\\{img_name}.jpg')
                    except:
                        urllib.request.urlretrieve(prd_img, f'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images\\{img_name}.png')
                    # upload images into s3 bucket
                if answer == 'yes':
                    self.uploadDirectory()
                else:
                    pass
        except:
            print('image download from site failed')


    def get_all_product(self):
        """
        scrape all required data from the site
        """
        
        all_product = self.driver.find_elements(by=By.XPATH, value="(//li[contains(@class,'productListProducts_product')])")
        
        for products in all_product:
            status = False
            #gets the product title and return only the text
            product_title= products.find_element(By.XPATH, ".//h3[@class='athenaProductBlock_productName']").text
            
            #gets the product price but it checks for the xpath for both
            
            try:
                product_price = products.find_element(By.XPATH,".//span[@class='athenaProductBlock_fromValue']").text
            except:
                product_price = products.find_element(By.XPATH,".//span[@class='athenaProductBlock_priceValue']").text
            
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
            self.avoid_rescrap(product_unik)
            
            # APPEND VARIOUS RETRIEVAL TO ITS RESPECTIVE DICTIONARY
            self.data['Unique_Id'].append(UniqueId)
            self.data['Product_Id'].append(product_unik)
            self.data['Product_Name'].append(product_title)
            self.data['Product_Price'].append(product_price)
            self.data['Product_Link'].append(product_link)
            self.data['Product_img'].append(product_img)
            self.data['Product_description'].append(product_text)

            raw_datas['Unique_Id'].append(UniqueId)
            raw_datas['Product_Id'].append(product_unik)
            raw_datas['Product_Name'].append(product_title)
            raw_datas['Product_Price'].append(product_price)
            raw_datas['Product_Link'].append(product_link)
            raw_datas['Product_img'].append(product_img)
            raw_datas['Product_description'].append(product_text)
            
            #this insert the data into the database if it doesn't already exist
            super().insert_into_database_noduplicate(product_unik,product_title,product_link,product_img)

            folder_product_unik = str(product_unik)

            self.avoid_rescrap(folder_product_unik)
            if self.rescrape_tag == False:
                #create a folder path and name for each product
                product_unik_path = f'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\{product_unik}'
                make_folder(product_unik_path)
                os.chdir(product_unik_path)
                # dump each as json file with data.json as file name
                with open('data.json', 'a') as f:
                    json.dump(raw_datas, f)
            else:
                print('value already exist so skipping')
                pass
            
            # save data into s3 bucket
            self.dump_raw_data_to_s3(raw_datas,product_unik)
            
            raw_datas.clear()
           

  

    def test(self):
        self.open_website()
        #self.driver.maximize_window()
        self.driver.implicitly_wait(20)
        self.accept_cookies()
        self.driver.implicitly_wait(20)
        self.click_on_vitamins()
        # self.click_on_view_all()
        self.scroll_down_to_last_page()
        self.driver.implicitly_wait(20)
        self.convert_to_dataframe()
        sleep(3)
        self.get_all_product()
        sleep(3)
        self.download_img()
        sleep(3)

       
        







if __name__ == '__main__':
    path = 'raw_data'
    def make_folder(path):
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            pass
    make_folder(path)
    data=scrapper()
    data.test()  
    


