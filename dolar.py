from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions
import os
from tabulate import tabulate

class BankBot():
    def __init__(self):
        chrome_options = Options()
        chrome_options.binary_location = os.getcwd() + os.sep + 'chrome-win' + os.sep + 'chrome.exe'
        chrome_options.add_argument('--lang=pt-BR')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-gpu')
        way = os.getcwd() + os.sep + 'chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path= way, options=chrome_options)
        
        self.wait = WebDriverWait(
            driver=self.driver,
            timeout=10,
            poll_frequency=1,
            ignored_exceptions=[NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException]
        )
    
    def Start(self):
        self.driver.get('https://www.bcb.gov.br/')
        self.GetElements()
        self.Done()
    
    def GetElements(self):
        prices = self.wait.until(expected_conditions.visibility_of_all_elements_located(
                        (By.XPATH, '//td[@class="text-right"]')))
        datas = self.wait.until(expected_conditions.visibility_of_all_elements_located(
                        (By.XPATH, '//td[@class="text-left"]')))
        self.title()
        self.ShowValues(prices, datas)

    def ShowValues(self, prices, datas):
        list_quotes = []
        dolar, euro, buy, sell = 'Dólar EUA', 'Euro', 'Compra (R$)', 'Venda (R$)' # titles
        # --- Dolar -->
        self.line()
        c = 0
        for cont in range(0, 4,2): # dolar values
            list_quotes.append([datas[c].text, prices[cont].text, prices[cont+1].text])
            c += 1
        
        print(tabulate(list_quotes,
                    headers=[dolar, buy, sell], tablefmt="psql", numalign="center"))

        # --- Euro -->
        list_quotes.clear()
        self.line()
    
        c = 2
        for cont in range(4, 8, 2): # euro values
            list_quotes.append([datas[c].text, prices[cont].text, prices[cont+1].text])
            c += 1
        
        print(tabulate(list_quotes,
                    headers=[euro, buy, sell], tablefmt="psql", numalign="center"))

        self.line()
        
    
    def Done(self):
        self.driver.quit()

    def line(self):
        print('_' * 45)
        print('')
    
    def title(self):
        print('''
  ____      _                                          _          _  ___  
 / ___|___ | |_ __ _  ___ ___   ___  ___   _ __   ___ | |_ __ _  / |/ _ \ 
| |   / _ \| __/ _` |/ __/ _ \ / _ \/ __| | '_ \ / _ \| __/ _` | | | | | |
| |__| (_) | || (_| | (_| (_) |  __/\__ \ | | | | (_) | || (_| | | | |_| |
 \____\___/ \__\__,_|\___\___/ \___||___/ |_| |_|\___/ \__\__,_| |_|\___/''')
        
if __name__ == "__main__":
    root = BankBot()
    root.Start()