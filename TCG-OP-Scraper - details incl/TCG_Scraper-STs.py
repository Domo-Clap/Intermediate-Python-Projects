########################################################################################################################
########################################################################################################################
########################################################################################################################

# Hosts a class that scrapes the TCGPlayer Website for OPTCG card data, including name, price, type, etc...
# THIS FILE ONLY CHECKS THE STRUCTURE DECK DATA. IT DOES NOT CHECK FOR MAIN LINE SET DATA
# Also hosts the main function for this project which runs the scraping process and converts the data into a readable
# format via the other file/class TransformData.

# Last updated 9/18/2024 by Dominic C. - First Iteration of Code for scraping the website for specifically structure deck
#                                        data. This uses the new way of gathering data built into the intitial TCG_Scraper.py file.
#                                        Also includes our TransformData_MySQL file which is used to push to our MYSQL DB

# Future Updates: Will eventually make the project connect to a database, load the scraped data into the database, and
#                   then post the data to a website.

########################################################################################################################
########################################################################################################################
########################################################################################################################

from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import TransformData
import TransformData_MYSQL


########################################################################################################################
########################################################################################################################
########################################################################################################################
class GetOnePieceInfo:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")  # Sometimes needed for headless mode
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        # Web Driver used to connect to our website
        self.driver = webdriver.Chrome(options=chrome_options)

        # Holds the cards for the current set, alongside the wanted info
        self.cardDict = {}

        self.loop_var = True

        # All of the structure dicts are different because of the way the data is formatted on the specific sites we scrape from
        # character card sites have slightly different data compared to the leader card sites, etc...

        # Dict used to assign the data for character cards
        self.charStructDict_counter = {0: "Card Name",
                                       1: "Inventory Price",
                                       2: "Market Price",
                                       3: "Set Name",
                                       4: "Card Text",
                                       5: "Rarity",
                                       6: "Card Set ID",
                                       7: "Card Color",
                                       8: "Card Type",
                                       9: "Card Cost",
                                       10: "Card Power",
                                       11: "SubTypes",
                                       12: "Counter",
                                       13: "Attribute"}

        self.charStructDict_no_counter = {0: "Card Name",
                                          1: "Inventory Price",
                                          2: "Market Price",
                                          3: "Set Name",
                                          4: "Card Text",
                                          5: "Rarity",
                                          6: "Card Set ID",
                                          7: "Card Color",
                                          8: "Card Type",
                                          9: "Card Cost",
                                          10: "Card Power",
                                          11: "SubTypes",
                                          12: "Attribute"}

        # Dict used to assign the data for leader cards
        self.leaderStructDict = {0: "Card Name",
                                 1: "Inventory Price",
                                 2: "Market Price",
                                 3: "Set Name",
                                 4: "Card Text",
                                 5: "Rarity",
                                 6: "Card Set ID",
                                 7: "Card Color",
                                 8: "Card Type",
                                 9: "Life",
                                 10: "Card Power",
                                 11: "SubTypes",
                                 12: "Attribute"}

        # Dict used to assign the data for the event cards
        self.eventStructDict = {0: "Card Name",
                                1: "Inventory Price",
                                2: "Market Price",
                                3: "Set Name",
                                4: "Card Text",
                                5: "Rarity",
                                6: "Card Set ID",
                                7: "Card Color",
                                8: "Card Type",
                                9: "Card Cost",
                                10: "SubTypes"}

        self.stageStructDict = {0: "Card Name",
                                1: "Inventory Price",
                                2: "Market Price",
                                3: "Set Name",
                                4: "Card Text",
                                5: "Rarity",
                                6: "Card Set ID",
                                7: "Card Color",
                                8: "Card Type",
                                9: "Card Cost",
                                10: "SubTypes"}

    # Function used to get the cards from the specific website. Runs through a loop that gets all of the elements from the specifc set/page of the set
    def get_cards(self, page_url):

        try:
            self.driver.get(page_url)

            # Wait until all cards from the indiv page are loaded in
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "product-card__product")))

            # Used to track if we can move to the next page and where we are when we regrab the page to avoid stale elements
            cardLoopVar = 0

            while True:
                # Get all of the cards on the current page
                all_cards = self.driver.find_elements(By.CLASS_NAME, "product-card__product")

                if cardLoopVar >= len(all_cards):
                    break

                try:

                    # Get the card name, price, marketprice, and set name before going into the details page of each card
                    card_name = all_cards[cardLoopVar].find_element(By.CLASS_NAME, "product-card__title")

                    try:
                        card_price = all_cards[cardLoopVar].find_element(By.CLASS_NAME,"inventory__price-with-shipping")

                    except NoSuchElementException:
                        card_price = None

                    try:
                        card_mprice = all_cards[cardLoopVar].find_element(By.CLASS_NAME,"product-card__market-price--value")

                    except NoSuchElementException:
                        card_mprice = None

                    card_set_name = all_cards[cardLoopVar].find_element(By.CLASS_NAME,"product-card__set-name__variant")

                    # Gets the text for each element
                    cName = card_name.text.strip()

                    if card_price is not None:

                        cPrice = card_price.text.strip()

                    if card_mprice is not None:

                        cMPrice = card_mprice.text.strip()

                    cSetName = card_set_name.text.strip()

                    # places them in our individual card/object dict
                    card_details = {"Inventory Price": cPrice,
                                    "Market Price": cMPrice,
                                    "Set Name": cSetName
                                    }

                    # Finds the first card in the all_cards list for the page. Then, clicks on it to locate to the next page
                    all_cards[cardLoopVar].find_element(By.CLASS_NAME, "product-card__title").click()

                    # Waits until the card details are on page
                    WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "product-details__name")))

                    time.sleep(2)

                    try:
                        card_text = self.driver.find_element(By.CLASS_NAME, "product__item-details__description")

                    except NoSuchElementException:
                        card_text = None

                    if card_text is not None:

                        card_text = card_text.text.strip()

                    card_details["Card Text"] = card_text

                    # Gets the unordered list on each card detail page
                    detailUL = self.driver.find_element(By.CLASS_NAME, "product__item-details__attributes")

                    # Gets the span elements inside the unordered list
                    span_elements = detailUL.find_elements(By.TAG_NAME, "span")

                    # print(span_elements)

                    card_type = None

                    # Looks at each card detail in the span_elements list
                    # Then, we compare the text value of the span/card detail to see what type of card it is
                    for span in span_elements:

                        # position 8 in dict is counter. if character card and the value of the span is not 0 and is equal to the key Counter
                        if 'character' == span.text.lower():

                            try:
                                counter_val = int(span_elements[7].text)
                                if counter_val > 0:
                                    card_type = "Character with Counter"
                                else:
                                    card_type = "Character without Counter"
                            except ValueError:
                                card_type = "Character without Counter"

                            break

                        elif 'event' == span.text.lower():
                            card_type = "Event"
                            break

                        elif 'leader' == span.text.lower():
                            card_type = "Leader"
                            break

                        elif 'stage' == span.text.lower():
                            card_type = "Stage"
                            break

                    # Next, we get all of the card details from the card page, and assign them to the specific dictionary
                    # depending on the card type we scanned for earlier
                    for index, span in enumerate(span_elements):

                        if card_type == "Character with Counter" and (index + 5) in self.charStructDict_counter:

                            key = self.charStructDict_counter[index + 5]
                            value = span.text.strip()

                            card_details[key] = value

                        elif card_type == "Character without Counter" and (index + 5) in self.charStructDict_no_counter:

                            key = self.charStructDict_no_counter[index + 5]
                            value = span.text.strip()

                            card_details[key] = value

                        elif card_type == "Event" and (index + 5) in self.eventStructDict:

                            key = self.eventStructDict[index + 5]
                            value = span.text.strip()

                            card_details[key] = value

                        elif card_type == "Leader" and (index + 5) in self.leaderStructDict:

                            key = self.leaderStructDict[index + 5]
                            value = span.text.strip()

                            card_details[key] = value

                        elif card_type == "Stage" and (index + 5) in self.stageStructDict:

                            key = self.stageStructDict[index + 5]
                            value = span.text.strip()

                            card_details[key] = value

                        else:

                            key = self.charStructDict_counter[index + 5]
                            value = span.text.strip()

                            card_details[key] = value


                    print(card_details)

                    self.cardDict[cName] = card_details

                    time.sleep(2)

                    # Goes back to main card page
                    self.driver.back()

                    WebDriverWait(self.driver, 20).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "product-card__product")))


                except Exception as e:
                    print(f"error: {e}")
                    continue

                cardLoopVar += 1

            print(self.cardDict)


        except Exception as e:
            print(f"Exception occurred: {e}")
            self.loop_var = False
            return

    # Makes it easier to stop the webdriver
    def stopDriver(self):
        self.driver.quit()


########################################################################################################################
########################################################################################################################
########################################################################################################################
# Function used to start the web scraping process. Is called in the main function
# Takes in the webpage URL to scrape, as well as the name of the card set, and the number/string associated with the set
# Will run through every page with card objects on the webpage until there are no more.
def StartScrape(setURL, setName, setNum):
    # Creates a class object to call the scrape actual selenium scrape functions
    scraper = GetOnePieceInfo()

    # Assigns the url to pass in
    base_URL = setURL

    try:

        # Loops until there are no more pages with card objects onm them
        page_url = f"{base_URL}?view=grid&productLineName=one-piece-card-game&page=1&setName={setName}&CardType=Character|Event|Leader|Stage"
            # Pulls in the data for the cards by using the dict from the scraper object
        scraper.get_cards(page_url)

        time.sleep(5)


    except KeyboardInterrupt:
        print("Interrupted by user, stopping....")

    # Stops the driver for the current card set
    finally:
        scraper.stopDriver()

    # Creates a data transformer object to transform our card data into a format for our database
    transformer = TransformData.TransformDictData()

    # Moves the returned card dict to a pandas df
    goodData = transformer.TransformToDF(scraper.cardDict, setNum)

    # Returns our final df for the set of cards
    return goodData


# Main function
if __name__ == '__main__':

    #ST01 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/starter-deck-1-straw-hat-crew", "starter-deck-1-straw-hat-crew", "ST-01")
    #ST02 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/starter-deck-2-worst-generation", "starter-deck-2-worst-generation", "ST-02")
    #ST03 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/starter-deck-3-the-seven-warlords-of-the-sea", "starter-deck-3-the-seven-warlords-of-the-sea", "ST-03")
    #ST04 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/starter-deck-4-animal-kingdom-pirates", "starter-deck-4-animal-kingdom-pirates", "ST-04")

    #ST05 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/starter-deck-5-film-edition", "starter-deck-5-film-edition", "ST-05")
    #ST06 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/starter-deck-6-absolute-justice", "starter-deck-6-absolute-justice", "ST-06")
    #ST07 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/starter-deck-7-big-mom-pirates", "starter-deck-7-big-mom-pirates", "ST-07")
    #ST08 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/starter-deck-8-monkeydluffy", "starter-deck-8-monkeydluffy", "ST-08")
    #ST09 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/starter-deck-9-yamato", "starter-deck-9-yamato", "ST-09")

    #ST10 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/ultra-deck-the-three-captains","ultra-deck-the-three-captains", "ST-10")
    #ST11 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/starter-deck-11-uta", "starter-deck-11-uta", "ST-11")
    #ST12 = StartScrape("https://www.tcgplayer.com/search/one-piece-card-game/starter-deck-12-zoro-and-sanji", "starter-deck-12-zoro-and-sanji", "ST-12")


    # Combines all of the card dataframes for each set into one large data frame.
    # Makes it easier to call the pushtodbTBL function when we want to load a new database table
    #finalDF = pandas.concat([])

    #print(finalDF)

    # csvFile = finalDF.to_csv('testCSV_dataST.csv')

    finalDF = pd.read_csv('OPTCG_Structure_Deck_Cards.csv')

    print(finalDF)

    # Needed a transform data object to move our data to the DB
    dbOP = TransformData_MYSQL.TransformDictData()

    dbOP.pushToSTTBL(finalDF)

    #time.sleep(10)

    #dbOP.pushToSTTBL(finalDF)

