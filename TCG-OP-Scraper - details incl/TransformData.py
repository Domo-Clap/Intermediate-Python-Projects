########################################################################################################################
########################################################################################################################
########################################################################################################################

# Hosts a class that contains functions to accept web-scraped data from the TCGScraper object, and transforms the data
# into a clean df using pandas. Also contains a testing function to turn the clean df into a csv file.

# Last updated 7/1/2024 by Dominic C. - First Iteration of Code for transforming the data from the scraped website.

# Future Updates: None at the moment for this specific file.

########################################################################################################################
########################################################################################################################
########################################################################################################################

import pandas as pd
import pyodbc
from datetime import date


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


    def createSTsTbl(self):

        tableName = "OPTCG_Structure_Deck_Cards"

        SERVER = 'DESKTOP-IKV9RTD\\DOMO_TEST_SERVER'
        DATABASE = 'OPTCG-Django-test'
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes'

        # Establish the connection
        conn = pyodbc.connect(connectionString)

        createQuery = f"""If NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{tableName}')
                            BEGIN
                	            EXEC('CREATE TABLE {tableName} (
                                     Card_ID int IDENTITY(1,1) PRIMARY KEY,
                                     Card_Name varchar(100),
                                     Inventory_Price Decimal(6, 2),
                                     Market_Price Decimal(6, 2),
                                     Set_Name varchar(70),
                                     Card_Text varchar(max),
                                     Set_ID varchar(5),
                                     Rarity varchar(5),
                                     Card_Set_ID varchar(10),
                                     Card_Color varchar(15),
                                     Card_Type varchar(25),
                                     Life INT,
                                     Card_Cost INT,
                                     Card_Power INT,
                                     Sub_Types varchar(150),
                                     Counter_Amount varchar(10),
                                     Attribute varchar(25),
                                     Date_Scraped DATE
                                 );')
                            END"""

        # Create a cursor object using the connection
        cursor = conn.cursor()

        cursor.execute(createQuery)

        conn.commit()

        conn.close()


    def pushToSTTBL(self, set_df):

        tableName = "OPTCG_Structure_Deck_Cards"

        SERVER = 'DESKTOP-IKV9RTD\\DOMO_TEST_SERVER'
        DATABASE = 'OPTCG-Django-test'
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes'

        # Establish the connection
        conn = pyodbc.connect(connectionString)

        # Create a cursor object using the connection
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
                                 Date_Scraped) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
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

        conn.close()


    def createSetTbl(self):
        # Basic table name with current date
        tableName = "OPTCG_Sets_Cards"

        SERVER = 'DESKTOP-IKV9RTD\\DOMO_TEST_SERVER'
        DATABASE = 'OPTCG-Django-test'
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes'

        # Establish the connection
        conn = pyodbc.connect(connectionString)

        createQuery = f"""If NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{tableName}')
                    BEGIN
        	            EXEC('CREATE TABLE {tableName} (
                             Card_ID int IDENTITY(1,1) PRIMARY KEY,
                             Card_Name varchar(100),
                             Inventory_Price Decimal(6, 2),
                             Market_Price Decimal(6, 2),
                             Set_Name varchar(70),
                             Card_Text varchar(max),
                             Set_ID varchar(5),
                             Rarity varchar(5),
                             Card_Set_ID varchar(10),
                             Card_Color varchar(15),
                             Card_Type varchar(25),
                             Life INT,
                             Card_Cost INT,
                             Card_Power INT,
                             Sub_Types varchar(150),
                             Counter_Amount varchar(10),
                             Attribute varchar(25),
                             Date_Scraped DATE
                         );')
                    END"""

        # Create a cursor object using the connection
        cursor = conn.cursor()

        cursor.execute(createQuery)

        conn.commit()

        conn.close()


    def pushToSetTbl(self, set_df):

        tableName = "OPTCG_Sets_Cards"

        SERVER = 'DESKTOP-IKV9RTD\\DOMO_TEST_SERVER'
        DATABASE = 'OPTCG-Django-test'
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes'

        # Establish the connection
        conn = pyodbc.connect(connectionString)

        # Create a cursor object using the connection
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
                         Date_Scraped) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
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

        conn.close()


    def updateMainTbl(self, set_df):

        tableName = "OPTCG_Prices_Main"

        SERVER = 'DESKTOP-IKV9RTD\\DOMO_TEST_SERVER'
        DATABASE = 'OPTCG-Django-test'
        connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes'

        # Establish the connection
        conn = pyodbc.connect(connectionString)

        # Create a cursor object using the connection
        cursor = conn.cursor()

        createQuery = f"""If NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{tableName}')
            BEGIN
        	    EXEC('CREATE TABLE {tableName} (
                        Card_ID int IDENTITY(1,1) PRIMARY KEY,
                        Card_Name varchar(100),
                        Inventory_Price Decimal(6, 2),
                        Market_Price Decimal(6, 2),
                        Set_Name varchar(70),
                        Set_ID varchar(5),
                        Rarity varchar(5),
                        Card_Set_ID varchar(10),
                        Card_Color varchar(15),
                        Card_Type varchar(25),
                        Life INT,
                        Card_Cost INT,
                        Card_Power INT,
                        Sub_Types varchar(150),
                        Counter_Amount varchar(10),
                        Attribute varchar(25),
                        Date_Scraped DATE
                );')
            END"""

        cursor.execute(createQuery)

        conn.commit()

        # `tempTblName = "#TempTbl"
        #
        # createTempTblQuery = f"""
        #     CREATE TABLE {tempTblName} (
        #         Card_ID int IDENTITY(1,1) PRIMARY KEY,
        #         Card_Name varchar(100),
        #         Inventory_Price Decimal(6, 2),
        #         Market_Price Decimal(6, 2),
        #         Set_Name varchar(70),
        #         Set_ID varchar(5),
        #         Rarity varchar(5),
        #         Card_Set_ID varchar(10),
        #         Card_Color varchar(15),
        #         Card_Type varchar(25),
        #         Life INT,
        #         Card_Cost INT,
        #         Card_Power INT,
        #         Sub_Types varchar(150),
        #         Counter_Amount varchar(10),
        #         Attribute varchar(25),
        #         Date_Scraped DATE
        #     )"""`

        # cursor.execute(createTempTblQuery)

        for _, row in set_df.iterrows():
            cursor.execute(f"""INSERT INTO {tableName}
                (
                         Card_Name,
                         Inventory_Price,
                         Market_Price,
                         Set_Name,
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
                         Date_Scraped) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
            """, (
                row["Card Name"],
                row["Inventory Price"],
                row["Market Price"],
                row["Set Name"],
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

        # mergeTblsQuery = f"""
        #     MERGE {tableName} AS target
        #     USING {tempTblName} AS source
        #     ON target.Card_Name = source.Card_Name
        #         AND target.Card_Set_ID = source.Card_Set_ID
        #     WHEN MATCHED THEN
        #         UPDATE SET
        #             target.Inventory_Price = source.Inventory_Price,
        #             target.Market_Price = source.Market_Price,
        #             target.Set_Name = source.Set_Name,
        #             target.Date_Scraped = source.Date_Scraped
        #     WHEN NOT MATCHED THEN
        #         Insert (Card_Name, Inventory_Price, Market_Price, Set_Name, Set_ID, Date_Scraped)
        #         VALUES (source.Card_Name, source.Inventory_Price, source.Market_Price, source.Set_Name, source.Set_ID, source.Date_Scraped);
        # """
        #
        # cursor.execute(mergeTblsQuery)
        #
        # cursor.execute(f"DROP TABLE {tempTblName}")

        # conn.commit()

        cursor.close()
        conn.close()

