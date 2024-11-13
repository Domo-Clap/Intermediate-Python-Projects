########################################################################################################################
########################################################################################################################
########################################################################################################################

import pandas as pd
import pyodbc
from datetime import date
import mysql.connector
import MySQLdb
import sshtunnel


########################################################################################################################
########################################################################################################################
########################################################################################################################

# Class for the transformData object. Made it easier to call certain functions related to cleaning/moving the data
class TransformDictData:
    def __init__(self):

        self.cardNames = []
        self.cardInfo = []


    def TransformToDF(self, CardDict, setNum):
        data = []

        for cardName, d in CardDict.items():
            inventoryPrice = d.get('Inventory Price', None)
            marketPrice = d.get('Market Price', None)
            cardSetName = d.get('Set Name', None)
            cardText = d.get('Card Text', None)
            rarity = d.get('Rarity', None)
            cardSID = d.get('Card Set ID', None)
            cardColor = d.get('Card Color', None)
            cardType = d.get('Card Type', None)
            leaderLife = d.get('Life', None)
            cardCost = d.get('Card Cost', None)
            cardPower = d.get('Card Power', None)
            subTypes = d.get('SubTypes', None)
            counterAmnt = d.get('Counter', 0)
            attrib = d.get('Attribute', None)

            data.append([cardName, inventoryPrice, marketPrice, cardSetName, cardText, setNum, rarity, cardSID, cardColor, cardType,
                         leaderLife, cardCost, cardPower, subTypes, counterAmnt, attrib])

        df = pd.DataFrame(data, columns=["Card Name", "Inventory Price", "Market Price", "Set Name", "Card Text", "Set ID", "Rarity",
                                         "Card Set ID", "Card Color", "Card Type", "Life", "Card Cost", "Card Power", "Sub Type(s)", "Counter Amount",
                                         "Attribute"])

        df["Inventory Price"] = df["Inventory Price"].str.replace("[\$,]", "", regex=True).astype(float).round(2)
        df["Market Price"] = df["Market Price"].str.replace("[\$,]", "", regex=True).astype(float).round(2)

        df['Date'] = date.today().strftime('%Y-%m-%d')

        return df




    def createSetTbl(self):

        tableName = "OPTCG_Sets_Cards"

        HOST = 'DomoTheSlime.mysql.pythonanywhere-services.com'
        DATABASE = 'DomoTheSlime$OPTCG-API-Data'
        USERNAME = 'DomoTheSlime'
        PASSWORD = '@Aether!Main333'

        # Establish the connection
        conn = mysql.connector.connect(

            host=HOST,
            user=USERNAME,
            password=PASSWORD,
            database=DATABASE

        )

        cursor = conn.cursor()

        createQuery = f"""
                CREATE TABLE IF NOT EXISTS {tableName} (
                    Card_ID INT AUTO_INCREMENT PRIMARY KEY,
                    Card_Name VARCHAR(100),
                    Inventory_Price DECIMAL(6, 2),
                    Market_Price DECIMAL(6, 2),
                    Set_Name VARCHAR(70),
                    Card_Text TEXT,
                    Set_ID VARCHAR(5),
                    Rarity VARCHAR(5),
                    Card_Set_ID VARCHAR(10),
                    Card_Color VARCHAR(15),
                    Card_Type VARCHAR(25),
                    Life INT,
                    Card_Cost INT,
                    Card_Power INT,
                    Sub_Types VARCHAR(150),
                    Counter_Amount VARCHAR(10),
                    Attribute VARCHAR(25),
                    Date_Scraped DATE
                );"""

        cursor.execute(createQuery)

        conn.commit()

        cursor.close()

        conn.close()


    def pushToSetTbl(self, set_df):

        tableName = "OPTCG_Sets_Cards"

        HOST = 'DomoTheSlime.mysql.pythonanywhere-services.com'
        DATABASE = 'DomoTheSlime$OPTCG-API-Data'
        USERNAME = 'DomoTheSlime'
        PASSWORD = '@Aether!Main333'

        # Establish the connection
        conn = mysql.connector.connect(

            host=HOST,
            user=USERNAME,
            password=PASSWORD,
            database=DATABASE

        )

        cursor = conn.cursor()

        for _, row in set_df.iterrows():
            cursor.execute(f"""INSERT INTO {tableName} (
                         Card_Name,
                         Inventory_Price,
                         Market_Price,
                         Set_Name,
                         Card_Text,
                         Set_ID,
                         Rarity,
                         Card_Set_ID,
                         Card_Color,
                         Card_Type,
                         Life,
                         Card_Cost,
                         Card_Power,
                         Sub_Types,
                         Counter_Amount,
                         Attribute,
                         Date_Scraped) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                row["Card Name"],
                row["Inventory Price"],
                row["Market Price"],
                row["Set Name"],
                row["Card Text"],
                row["Set ID"],
                row["Rarity"],
                row["Card Set ID"],
                row["Card Color"],
                row["Card Type"],
                row["Life"],
                row["Card Cost"],
                row["Card Power"],
                row["Sub Type(s)"],
                row["Counter Amount"],
                row["Attribute"],
                row["Date"]
            ))

        conn.commit()

        cursor.close()

        conn.close()



    def createSTsTbl(self):

        tableName = "OPTCG_Structure_Deck_Cards"

        HOST = 'DomoTheSlime.mysql.pythonanywhere-services.com'
        DATABASE = 'DomoTheSlime$OPTCG-API-Data'
        USERNAME = 'DomoTheSlime'
        PASSWORD = '@Aether!Main333'

        # Establish the connection
        conn = mysql.connector.connect(

            host=HOST,
            user=USERNAME,
            password=PASSWORD,
            database=DATABASE

        )

        cursor = conn.cursor()

        createQuery = f"""CREATE TABLE IF NOT EXISTS {tableName} (
                    Card_ID INT AUTO_INCREMENT PRIMARY KEY,
                    Card_Name VARCHAR(100),
                    Inventory_Price DECIMAL(6, 2),
                    Market_Price DECIMAL(6, 2),
                    Set_Name VARCHAR(70),
                    Card_Text TEXT,
                    Set_ID VARCHAR(5),
                    Rarity VARCHAR(5),
                    Card_Set_ID VARCHAR(10),
                    Card_Color VARCHAR(15),
                    Card_Type VARCHAR(25),
                    Life INT,
                    Card_Cost INT,
                    Card_Power INT,
                    Sub_Types VARCHAR(150),
                    Counter_Amount VARCHAR(10),
                    Attribute VARCHAR(25),
                    Date_Scraped DATE"""

        cursor.execute(createQuery)

        conn.commit()

        cursor.close()

        conn.close()


    def pushToSTTBL(self, set_df):

        tableName = "OPTCG_Sets_Cards"

        HOST = 'DomoTheSlime.mysql.pythonanywhere-services.com'
        DATABASE = 'DomoTheSlime$OPTCG-API-Data'
        USERNAME = 'DomoTheSlime'
        PASSWORD = '@Aether!Main333'

        # Establish the connection
        conn = mysql.connector.connect(

            host=HOST,
            user=USERNAME,
            password=PASSWORD,
            database=DATABASE

        )

        cursor = conn.cursor()

        for _, row in set_df.iterrows():
            cursor.execute(f"""INSERT INTO {tableName} (
                         Card_Name,
                         Inventory_Price,
                         Market_Price,
                         Set_Name,
                         Card_Text,
                         Set_ID,
                         Rarity,
                         Card_Set_ID,
                         Card_Color,
                         Card_Type,
                         Life,
                         Card_Cost,
                         Card_Power,
                         Sub_Types,
                         Counter_Amount,
                         Attribute,
                         Date_Scraped) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                row["Card Name"],
                row["Inventory Price"],
                row["Market Price"],
                row["Set Name"],
                row["Card Text"],
                row["Set ID"],
                row["Rarity"],
                row["Card Set ID"],
                row["Card Color"],
                row["Card Type"],
                row["Life"],
                row["Card Cost"],
                row["Card Power"],
                row["Sub Type(s)"],
                row["Counter Amount"],
                row["Attribute"],
                row["Date"]
            ))

        conn.commit()

        cursor.close()

        conn.close()

