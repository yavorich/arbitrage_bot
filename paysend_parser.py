from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re

url = 'https://paysend.com/ru-us'


def parse_ps(driver):
    driver.get(url)
    driver.implicitly_wait(10)
    sel = Selector(text=driver.page_source)
    if sel.xpath('//span[contains(text(), "Разрешить все файлы cookie")]'):
        element = driver.find_element(By.XPATH, '//span[contains(text(), "Разрешить все файлы cookie")]')
        element.click()
        driver.implicitly_wait(5)
    if sel.xpath('(//span[@id="iso_country_from"])[1]/text()').extract_first() != 'RUB':
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20)
                              .until(EC.element_to_be_clickable((By.XPATH, '(//span[@id="iso_country_from"])[1]'))))
        driver.implicitly_wait(5)
        element = driver.find_element(By.XPATH, '//span[@class="value" and contains(text(), "Россия")]')
        element.click()
        driver.implicitly_wait(5)
    sel = Selector(text=driver.page_source)
    if sel.xpath('(//span[@id="iso_country_from"])[2]/text()').extract_first() != 'UZS':
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20)
                              .until(EC.element_to_be_clickable((By.XPATH, '(//span[@id="iso_country_from"])[2]'))))
        driver.implicitly_wait(5)
        element = driver.find_element(By.XPATH, '//span[@class="value" and contains(text(), "Узбекистан")]')
        element.click()
        driver.implicitly_wait(5)
    sel = Selector(text=driver.page_source)
    item = sel.xpath('//span[@class="foo"]/text()').extract_first()
    currency = re.findall(r'[0-9/.]+', item)[-1]
    #save(currency)
    return float(currency)


if __name__ == '__main__':
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(executable_path='C:/ChromeDriver/chromedriver.exe', options=op)
    while True:
        #try:
        parse_ps(driver)
        #except:
        #    print('Something went wrong')
        #    time.sleep(5)
        #   continue
        time.sleep(120)