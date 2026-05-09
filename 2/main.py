from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


PRICE_TAG_CLASS="ds-text_color_price-term"
RATING_CLASS="ds-rating__value"


def parse_prices(driver):
    price_tags=driver.find_elements(By.CLASS_NAME,PRICE_TAG_CLASS)
    for price_tag in price_tags:
        price=price_tag.text.replace("\u2006","")
        if price.isnumeric():
            prices.append(int(price))
    return prices

def parse_ratings(driver):
    ratings=driver.find_elements(By.CLASS_NAME,RATING_CLASS)
    ratings_numeric=[]
    for rating in ratings:
        ratings_numeric.append(float(rating.text))
    return ratings_numeric
driver = webdriver.Firefox()
query='фен'
pages_count=3
prices=[]
ratings=[]
for page_number in range(1,pages_count+1):
    driver.get(f"https://market.yandex.ru/search?text={query}&page={page_number}")
    prices+=parse_prices(driver)
    ratings+=parse_ratings(driver)
    driver.implicitly_wait(0.5)
driver.close()

with open("parse_result.csv","a") as output_file:    
    print(query,end=',',file=output_file)
    print(len(prices),end=',',file=output_file)
    print(sum(prices)/len(prices),end=',',file=output_file)
    print(max(prices),end=',',file=output_file)
    print(sum(ratings)/len(ratings),end='\n',file=output_file)

