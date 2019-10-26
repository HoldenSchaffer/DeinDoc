import pandas as pd


def createItemDictFromCSV():
    items = {}
    df = pd.read_csv("Products.csv")
    for index, row in df.iterrows():
        items[row['Name']] = Item(row['Name'], row['Price'], row['Description'], row['Link'], row['Disease'])
    return items

def newItemToCSV(name, price, description, link, disease):
    df = pd.read_csv("Products.csv")
    df.loc[len(df)] = [name, price, description, link, disease]
    df.to_csv('Products.csv', index=False)

def delItemFromCSV(name):
    df = pd.read_csv("Products.csv")
    df = df.drop(df[df.Name == name].index)
    df.to_csv('Products.csv', index=False)
              
class Item:
    def __init__(self, name, price, description, link, disease):
        self.name = name
        self.price = price
        self.description = description
        self.link = link
        self.disease = disease
