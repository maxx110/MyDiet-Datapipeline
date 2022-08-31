from cgitb import text
import os
from this import d
from time import sleep, time
from tkinter import image_names
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
import uuid
import json
import urllib.request
import boto3
import glob
import connection
import psycopg2
import psycopg2.extras as extras
import pandas as pd
import connection
from connection import Migration








class scrapper():

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
        locate_vitamins = self.driver.find_element(By.XPATH,"//*[@id='mainContent']/div[2]/a[4]")
        locate_vitamins.click()

    def scroll_down_to_last_page(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)

    def click_on_view_all(self):
        locate_view_all = self.driver.find_element(By.XPATH,"//a[normalize-space()='View all']")
        locate_view_all.click()

    
    def convert_to_dataframe(self):
        df = pd.DataFrame.from_dict(self.data, orient='index')
        data_frame = df.transpose()
        #Migration.create_table(self)
        print(data_frame)
        # Migration.con_database()
        # Migration.insert_df(data_frame)
        return data_frame

    # def insert_df(df,table,cur):
    #     if len(df)>0:
    #         df_columns = list(df)
    #         #create (col1,col2...)
    #         columns = ','.join(df_columns)
    #         #create values per column
    #         values = 'VALUES({})'.format(','.join(['%s' for _ in df_columns]))
    #         #create insert into table column and values
    #         insert_statement = 'INSERT INTO {} ({}) {}'.format(table,columns,values)
    #         cur.execute('truncate' + table + ';') #avoids duplicate
    #         cur = conn.cursor()
    #         psycopg2.extras.execute_batch(cur,insert_statement,df.values)
    #     conn.commit()
    

    # def upload_s3_bucket(self,s3_filename,stored_name):
    #     """
    #     uploads files into s3 bucket
    #     """
    #     bucket_name = 'aicorbuc'
    #     s3 = boto3.client('s3')
    #     s3.put_object(Body=json.dumps(s3_filename),Bucket=bucket_name,Key= f'website_data/{stored_name}')
        


    # def get_all_buck():
    #     """
    #     lists all buckets in s3
    #     """
    #     s3_obj = boto3.resource('s3')
    #     for elements in s3_obj.buckets.all():
    #         print(elements.name)
        
    # def uploadDirectory(self):
    #     s3= boto3.client('s3')
    #     bucket_name = 'aicorbuc'
    #     files = glob.glob('C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images\\*')
        
    #     for file in files:
    #         file_name = file.split('-')[-1]
    #         s3.upload_file(file,bucket_name,f'website_data/images/{file_name}')

           



    # def download_img(self):
    #     path3 = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data'
    #     os.chdir(path3)
    #     image_path = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images'
        
    #     if not os.path.exists(path3):
    #         os.makedirs(image_path) 
    #     else:
    #         pass

    #     #path4 = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images'
    #     # os.chdir(path4)
    #     # for i in self.img:
    #     #     #lnum = len(self.img)
    #     #     #filename = i.split('-'[-1])
    #     #     urllib.request.urlretrieve(i,f'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images\\a.jpg')

        
        # all_product = self.driver.find_elements(by=By.XPATH, value="//li[contains(@class,'productListProducts_product')]")
        # bucket_name = 'aicorbuc'
        # # s3 = boto3.client('s3')
        
        # for i in all_product:
            
        #     if not os.path.exists(image_path):
        #         os.makedirs(image_path) 
        #     img = i.find_element(By.XPATH, ".//div[@class='athenaProductBlock_imageContainer']")
        #     a_tag = img.find_elements(By.TAG_NAME,'img')
        #     #print(a_tag)
        #     for i in a_tag:
        #         prd_img= i.get_attribute('src')
        #         #print(prd_img)
        #         img_name = prd_img.split('/')[-1]
        #         try:
        #             urllib.request.urlretrieve(prd_img, f'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images\\{img_name}.jpg')
        #         except:
        #             urllib.request.urlretrieve(prd_img, f'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images\\{img_name}.png')
        #         #self.uploadDirectory(image_path,bucket_name)


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
            
            # #gets the product description
            # try:
            #     product_text= products.find_element(By.XPATH, ".//span[@class='papBanner_text']").text           
            # except:
            #     pass
            
            # raw_datas = {'Unique_Id': [], 'Product_Id': [], 'Product_Name': [], 'Product_Price': [], \
            # 'Product_Link': [], 'Product_img': [],'Product_description': []}

            # APPEND VARIOUS RETRIEVAL TO ITS RESPECTIVE DICTIONARY
            self.data['Unique_Id'].append(UniqueId)
            self.data['Product_Id'].append(product_unik)
            self.data['Product_Name'].append(product_title)
            #self.data['Product_Price'].append(product_price)
            self.data['Product_Link'].append(product_link)
            self.data['Product_img'].append(product_img)
           # self.data['Product_description'].append(product_text)

            # raw_datas['Unique_Id'].append(UniqueId)
            # raw_datas['Product_Id'].append(product_unik)
            # raw_datas['Product_Name'].append(product_title)
            # #raw_datas['Product_Price'].append(product_price)
            # raw_datas['Product_Link'].append(product_link)
            # raw_datas['Product_img'].append(product_img)
            # #raw_datas['Product_description'].append(product_text)

            # #appends web_image to self.image
            # self.img.append(product_img)

            # raw_data_path = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data'
            # os.chdir(raw_data_path)
            # os.mkdir(product_unik)
            # product_unik_path = f'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\{product_unik}'
            # os.chdir(product_unik_path)
            
            # with open('data.json', 'a') as f:
            #     json.dump(raw_datas, f)
            # bucket_name = 'aicorbuc'
            # s3 = boto3.client('s3')
            # data = json.dumps(raw_datas)
            # s3.put_object(Body=json.dumps(data),Bucket=bucket_name,Key= f'website_data/{product_unik}')

            #raw_datas.clear()

   
        
            
            

            
           
            

            

            

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
        # sleep(5)
        self.get_all_product()
        # #print(self.data)
        # # #sleep(5)
        # # #self.driver.close()
        # # #print(self.data)
        # # #print(self.img)
        # # #self.download_image()
        # # #self.download_img()
        # # sleep(10)
        # # self.uploadDirectory()
        # #connection.name()
        self.convert_to_dataframe()
        # #Migration.con_database()
        # #Migration.insert_df()
        #print(self.data)
        







if __name__ == '__main__':
    path = 'raw_data'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        pass
    data=scrapper()
    data.test()    


