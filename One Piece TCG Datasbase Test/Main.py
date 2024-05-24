import mysql.connector
import pandas as pd

import tkinter as tk
from tkinter import *
from tkinter import scrolledtext

root = Tk()
root.title('Prototype Database App')
root.geometry('400x75')


icon = "C:/Users/Dominic/PycharmProjects/One Piece TCG Datasbase Test/One_Piece_TCG_Icon.ico"
root.iconbitmap(icon)

connection = mysql.connector.connect(user='root', password='@12RazorFidgetSpinner98',
                                     host='localhost', database='one_piece_tcg_cards')

myCursor = connection.cursor()

baseQuery = ("SELECT * FROM OP_01 WHERE 1=1")

color_options = ['red', 'blue', 'green', 'purple']
rarity_options = ['Common', 'Uncommon', 'Super Rare', 'Secret Rare']
card_type_options = ['Leader', 'Character', 'Event']
cost_options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
power_options = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000]
attribute_options = ['Special', 'Strike', 'Slash', 'Wisdom', 'Ranged']
hasTrigger_options = [True, False]
counter_amount_options = [0, 1000, 2000]


myCursor.execute(baseQuery)

data = myCursor.fetchall()

df = pd.DataFrame(data, columns=['Card Id', 'Card Type', 'Card Name', 'Set ID', 'Rarity', 'Cost', 'Power', 'hasCounter',
                                 'Counter Amount', 'Attribute', 'Color', 'isDualColor', 'Dual Color', 'hasTrigger'])

def apply_filter():
    selected_color = colorChoice.get()
    selected_rarity = rarityChoice.get()
    selected_card_type = cardTypeChoice.get()
    selected_cost = costChoice.get()
    selected_power = powerChoice.get()
    selected_attribute = attributeChoice.get()
    selected_hasTrigger = hasTriggerChoice.get()
    selected_counterAmount = counterAmountChoice.get()

    query = baseQuery

    if selected_color:
        query += " AND Color = '%s'" % selected_color

        print(query)
    if selected_rarity:
        query += " AND Rarity = '%s'" % selected_rarity

    if selected_card_type:
        query += " AND card_type = '%s'" % selected_card_type

    if selected_cost:
        query += " AND cost = '%s'" % selected_cost

    if selected_power:
        query += " AND power = '%s'" % selected_power

    if selected_attribute:
        query += " AND attribute = '%s'" % selected_attribute

    if selected_hasTrigger:
        query += " AND hasTrigger = '%s'" % selected_hasTrigger

    if selected_counterAmount:
        query += " AND counter_amount = '%s'" % selected_counterAmount

    myCursor.execute(query)
    data = myCursor.fetchall()
    df_filtered = pd.DataFrame(data,
                      columns=['Card Id', 'Card Type', 'Card Name', 'Set ID', 'Rarity', 'Cost', 'Power', 'hasCounter',
                               'Counter Amount', 'Attribute', 'Color', 'isDualColor', 'Dual Color', 'hasTrigger'])

    update_display(df_filtered)

def update_display(df):
    databaseDisplay.delete(1.0, tk.END)
    databaseDisplay.insert(tk.END, df.to_string())

def display_Database():
    dialog = tk.Toplevel(root)
    dialog.title("One Piece TCG Cards")
    dialog.geometry("1650x650")

    iconInner = "C:/Users/Dominic/PycharmProjects/One Piece TCG Datasbase Test/One_Piece_TCG_Icon.ico"
    dialog.iconbitmap(iconInner)

    global colorChoice, rarityChoice, cardTypeChoice, costChoice, powerChoice, hasCounterChoice, attributeChoice,\
        hasTriggerChoice, counterAmountChoice, databaseDisplay

    colorChoice = tk.StringVar(dialog)
    colorChoice.set("")

    rarityChoice = tk.StringVar(dialog)
    rarityChoice.set("")

    cardTypeChoice = tk.StringVar(dialog)
    cardTypeChoice.set('')

    costChoice = tk.StringVar(dialog)
    costChoice.set('')

    powerChoice = tk.StringVar(dialog)
    powerChoice.set('')

    attributeChoice = tk.StringVar(dialog)
    attributeChoice.set('')

    hasTriggerChoice = tk.StringVar(dialog)
    hasTriggerChoice.set('')

    counterAmountChoice = tk.StringVar(dialog)
    counterAmountChoice.set('')

    color_filter_label = Label(dialog, text="Color: ")
    color_filter_label.grid(column=0, row=0, pady=5)

    color_filter = OptionMenu(dialog, colorChoice, *color_options)
    color_filter.grid(column=0, row=1, pady=5)

    rarity_filter_label = Label(dialog, text="Rarity: ")
    rarity_filter_label.grid(column=1, row=0, pady=5)

    rarity_filter = OptionMenu(dialog, rarityChoice, *rarity_options)
    rarity_filter.grid(column=1, row=1, pady=5)

    card_type_filter_label = Label(dialog, text="Card Type: ")
    card_type_filter_label.grid(column=2, row=0, pady=5)

    card_type_filter = OptionMenu(dialog, cardTypeChoice, *card_type_options)
    card_type_filter.grid(column=2, row=1, pady=5)

    cost_filter_label = Label(dialog, text="Card Cost: ")
    cost_filter_label.grid(column=3, row=0, pady=5)

    cost_filter = OptionMenu(dialog, costChoice, *cost_options)
    cost_filter.grid(column=3, row=1, pady=5)

    power_filter_label = Label(dialog, text="Card Power: ")
    power_filter_label.grid(column=4, row=0, pady=5)

    power_filter = OptionMenu(dialog, powerChoice, *power_options)
    power_filter.grid(column=4, row=1, pady=5)

    attribute_filter_label = Label(dialog, text="Card Attribute: ")
    attribute_filter_label.grid(column=5, row=0, pady=5)

    attribute_filter = OptionMenu(dialog, attributeChoice, *attribute_options)
    attribute_filter.grid(column=5, row=1, pady=5)

    trigger_filter_label = Label(dialog, text="Has a Trigger: ")
    trigger_filter_label.grid(column=6, row=0, pady=5)

    trigger_filter = OptionMenu(dialog, hasTriggerChoice, *hasTrigger_options)
    trigger_filter.grid(column=6, row=1, pady=5)

    counter_amount_filter_label = Label(dialog, text="Counter Amount: ")
    counter_amount_filter_label.grid(column=7, row=0, pady=5)

    counter_amount_filter = OptionMenu(dialog, counterAmountChoice, *counter_amount_options)
    counter_amount_filter.grid(column=7, row=1, pady=5)

    filterBTN = Button(dialog, text="Filter", command=apply_filter)
    filterBTN.grid(column=0, row=3, padx=5, pady=5)

    databaseDisplay = scrolledtext.ScrolledText(dialog, wrap=tk.WORD, width=200, height=30)
    databaseDisplay.grid(row=4, column=0, padx=5,pady=5, columnspan=10)

    apply_filter()


headerLabel = Label(root, text="One Piece TCG Card Database", font=('Cosmic Sans', 18, 'bold'))
headerLabel.pack()

displayBTN = Button(root, text="Display Database", command=display_Database)
displayBTN.pack()


root.mainloop()


