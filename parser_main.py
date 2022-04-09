from selenium.webdriver.common.by import By

from config import DRIVER_PATH, URL
from selenium import webdriver
from db import find_all_search, Sneakers


class ParseSneakers:
    def __init__(self, url, bot=None):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.driver.minimize_window()
        self.url = url
        self.bot = bot

    def __del__(self):
        self.driver.close()

    async def parse(self):
        global name, price
        search_models = find_all_search()

        for page in range(1, 5):
            print(self.url.format(page))
            self.driver.get(self.url.format(page))
            # items = len(self.driver.find_elements_by_class_name('card '))
            items_price = self.driver.find_elements(By.XPATH, '//*[@class="container productListConteiner '
                                                              'product-list-wrapper"]//span[@class="card__price-sum"]')
            items_name = self.driver.find_elements(By.XPATH, '//*[@class="container productListConteiner '
                                                             'product-list-wrapper"]//b[@class="nc"]')
            items_url = self.driver.find_elements(By.XPATH, '//*[@class="container productListConteiner '
                                                            'product-list-wrapper"]//a[@class="link link--big '
                                                            'link--inverted link--blue"]')
            for item in items_price:
                try:
                    price = item.text.split('₴')[0].replace(' ', '')
                    index_price = items_price.index(item)
                    name = items_name[index_price].text
                    url = items_url[index_price].get_attribute("href")
                except:
                    price = 0
                    name = ''
                    url = ''
                try:
                    sneakers = Sneakers.select().where(Sneakers.title == name).get()
                    sneakers.url = url
                    sneakers.price = price
                    sneakers.save()
                except:
                    rec = Sneakers(title=name, url=url, price=price)
                    rec.save()

            pass
