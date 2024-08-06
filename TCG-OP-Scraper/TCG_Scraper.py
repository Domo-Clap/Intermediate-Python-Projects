#######################################################################################################################
#######################################################################################################################

# Hosts a class that scrapes the TCGPlayer Website for OP-01 card names, inventory prices, and market prices.
# Also hosts the main function for this project which runs the scraping process and converts the data into a readable
# format via the other file/class TransformData.

# Last updated 7/1/2024 by Dominic C. - First Iteration of Code for scraping the website.

# Future Updates: Will eventually make the project connect to a database, load the scraped data into the database, and
#                   then post the data to a website.

#######################################################################################################################
#######################################################################################################################

from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import requests
import TransformData


class GetOnePieceInfo():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)

        self.cardDict = {}

        self.loop_var = True

    def get_cards(self, page_url):

        try:
            self.driver.get(page_url)

            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "product-card__product")))

            all_cards = self.driver.find_elements(By.CLASS_NAME, "product-card__product")

            print(all_cards)

            if not all_cards:
                print(f"No cards found on page: {page_num}")

            for card in all_cards:
                card_name = card.find_element(By.CLASS_NAME, "product-card__title")
                card_price = card.find_element(By.CLASS_NAME, "inventory__price-with-shipping")
                card_mprice = card.find_element(By.CLASS_NAME, "product-card__market-price--value")

                print(card_name.text)
                print(card_price.text)
                print(card_mprice.text)

                cName = card_name.text.strip()

                cPrice = card_price.text.strip()
                cMPrice = card_mprice.text.strip()

                self.cardDict[cName] = {"Inventory Price": cPrice, "Market Price": cMPrice}

            print(self.cardDict)

        except Exception as e:
            print(f"Exception occurred: {e}")
            self.loop_var = False
            return

    def stopDriver(self):
        self.driver.quit()




def StartScrape(setURL, setName):
    scraper = GetOnePieceInfo()

    base_URL = setURL

    try:

        page_num = 1

        while scraper.loop_var:
            page_url = f"{base_URL}?view=grid&productLineName=one-piece-card-game&setName={setName}&page={page_num}"
            scraper.get_cards(page_url)

            time.sleep(20)

            page_num += 1

    except KeyboardInterrupt:
        print("Interrupted by user, stopping....")

    finally:
        scraper.stopDriver()

    print(scraper.cardDict)

    transformer = TransformData.TransformDictData()

    goodData = transformer.TransformToDF(scraper.cardDict)

    print(goodData)

    transformer.ExportDF(goodData, setName)

    return goodData

    # HTML_Data = transformer.PutinHTML(goodData)

    # return HTML_Data


if __name__ == '__main__':
    OP01 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/romance-dawn", "romance-dawn")
    OP02 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/paramount-war", "paramount-war")
    OP03 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/pillars-of-strength", "pillars-of-strength")
    # OP04 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/kingdoms-of-intrigue", "kingdoms-of-intrigue")
    # OP05 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/awakening-of-the-new-era", "awakening-of-the-new-era")

    print(OP01)
    print(OP02)
    print(OP03)
