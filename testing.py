from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()

driver.get('https://www.myprotein.com/')
accept_cook= driver.find_element(By.XPATH,'//*[@id="home"]/div[4]/div/div[2]/button')
accept_cook.click()
accept_cookies= driver.find_element(By.XPATH,"//*[@id='home']/div[1]/div/div/div[2]/button")
accept_cookies.click()

locate_vitamins = driver.find_element(By.XPATH,"//*[@id='mainContent']/div[2]/a[4]")
locate_vitamins.click()