#######################################################################################################################
#######################################################################################################################

# Hosts a class that contains functions to accept web-scraped data from the TCGScraper object, and transforms the data
# into a clean df using pandas. Also contains a testing function to turn the clean df into a csv file.

# Last updated 7/1/2024 by Dominic C. - First Iteration of Code for transforming the data from the scraped website.

# Future Updates: None at the moment for this specific file.

#######################################################################################################################
#######################################################################################################################

import pandas as pd


class TransformDictData():
    def __init__(self):
        self.cardNames = []
        self.cardInfo = []

    def TransformToDF(self, CardDict):
        data = []
        for cardName, d in CardDict.items():
            inventoryPrice = d.get('Inventory Price', None)
            marketPrice = d.get('Market Price', None)

            data.append([cardName, inventoryPrice, marketPrice])

        df = pd.DataFrame(data, columns=["Card Name", "Inventory Price", "Market Price"])
        return df

    def ExportDF(self, cardDF, setName):
        cardDF.to_csv(f"One Piece - {setName} - Card Set Data.csv", index=False)

    def PutinHTML(self, cardDF):
        return cardDF.to_html(classes='data', header='true', index=False)

