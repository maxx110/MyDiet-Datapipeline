import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
import urllib.request





class s3_functions:
    def __init__(self):
        #self.driver =webdriver.Edge()
        #self.all_product = self.driver.find_elements(by=By.XPATH, value="//li[contains(@class,'productListProducts_product')]")
        self.bucket_name = 'aicorbuc'
        
    
    def make_folder(self,path):
        try:
            os.makedirs(path,exist_ok= True)
        except OSError as error:
            print("Directory '%s' cannot be created" % path)
            
    def download_image_locally(self):
        all_product = self.driver.find_elements(by=By.XPATH, value="//li[contains(@class,'productListProducts_product')]")
        #bucket_name = 'aicorbuc'
        # s3 = boto3.client('s3')
        image_path = 'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images'
        for i in self.all_product:
            self.make_folder(image_path)
            # if not os.path.exists(image_path):
            #     os.makedirs(image_path) 
            img = i.find_element(By.XPATH, ".//div[@class='athenaProductBlock_imageContainer']")
            a_tag = img.find_elements(By.TAG_NAME,'img')
            #print(a_tag)
            for i in a_tag:
                prd_img= i.get_attribute('src')
                #print(prd_img)
                img_name = prd_img.split('/')[-1]
                try:
                    urllib.request.urlretrieve(prd_img, f'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images\\{img_name}.jpg')
                except:
                    urllib.request.urlretrieve(prd_img, f'C:\\Users\\Maud\\Desktop\\python\\data_pipelines\\data_pipeline\\Scripts\\raw_data\\images\\{img_name}.png')
                #self.uploadDirectory(image_path,bucket_name)

# s3_func = s3_functions()
# s3_func.download_image_locally()