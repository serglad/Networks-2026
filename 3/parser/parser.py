import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from fastapi import FastAPI
import psycopg2
import psycopg2.extras
import dotenv

dotenv.load_dotenv(".env")

PRICE_TAG_CLASS = "ds-text_color_price-term"
RATING_CLASS = "ds-rating__value"

app = FastAPI()


@app.get("/parse_request")
def parse(query: str, pages_count: int = 0):
    def parse_prices(driver):
        price_tags = driver.find_elements(By.CLASS_NAME, PRICE_TAG_CLASS)
        for price_tag in price_tags:
            price = price_tag.text.replace("\u2006", "")
            if price.isnumeric():
                prices.append(int(price))
        return prices

    def parse_ratings(driver):
        ratings = driver.find_elements(By.CLASS_NAME, RATING_CLASS)
        ratings_numeric = []
        for rating in ratings:
            ratings_numeric.append(float(rating.text))
        return ratings_numeric

    pages_count = max(1, pages_count)
    driver = webdriver.Firefox()
    prices = []
    ratings = []
    for page_number in range(1, pages_count + 1):
        driver.get(
            f"https://market.yandex.ru/search?text={query}&page={page_number}"
        )
        prices += parse_prices(driver)
        ratings += parse_ratings(driver)
        driver.implicitly_wait(0.5)
    driver.close()
    if len(prices) == 0:
        prices=[-1]
    if len(ratings) == 0:
        ratings=[-1]
    submit(
        query,
        len(prices),
        sum(prices) / len(prices),
        max(prices),
        sum(ratings) / len(ratings),
        datetime.today().strftime("%Y-%m-%d"),
    )
    return "OK"


def submit(
    query: str,
    amount_parsed: int,
    avg_price: float,
    max_price: int,
    avg_rating: float,
    time,
):
    try:
        with psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
        ) as conn:
            print("Connection successful!")
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO parser_results(query, amount_parsed, "
                    "avg_price, max_price, avg_rating, time)\n"
                    f"VALUES ('{query}', {amount_parsed}, {avg_price}, "
                    f"{max_price}, {avg_rating}, '{str(time)}')"
                )
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")


@app.get("/get")
def get(query: str = None):
    result = dict()
    try:
        with psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
        ) as conn:
            print("Connection successful!")
            with conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            ) as cur:
                request = (
                    "SELECT query, amount_parsed, avg_price, "
                    "max_price, avg_rating, time FROM parser_results"
                )
                if query is not None:
                    request += f"\nWHERE query='{query}'"
                cur.execute(request)
                result = cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
    return result