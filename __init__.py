import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd

import utils
import re

def main1():
    list1 = pd.read_csv("list part 1 missing values.csv")
    print(list1.head(8))

    list1.to_csv("list part 1 (MOD).csv")

def dropCols(df, *cols):
    for col in cols:
        df = df.drop(col, 1)

    return df

def seperateCoords(df):
    def parseCoord(string):
        ltt = re.search(r'^.*?(?=;)', string).group()
        lng = re.search(r'(?<=;).*?(?=;)', string).group()
        acc = re.search(r'(?<=;).*?$', string.replace(lng+";", "")).group()

        return ltt, lng, acc

    df["lat"], df["long"], df["acc"] = zip(*df["location"].map(parseCoord))
    return df

def main2():
    def viewDf():
        print(list2.head(8))

    list2 = pd.read_csv("list part 2 (MOD).csv")
    ## Remove the CSV "unnamed columns"
    list2 = list2.loc[:, ~list2.columns.str.match('Unnamed')] 

    # for col in list2.columns:
    #     # print(list2[col])
    #     try:
    #         print(col + " - " + str(pd.isna(list2[col])))
    #         # print(col + " - " + str(list2[col].value_counts()["Convenience stall"]))
    #     except:
    #         print(col + " - None.")

    """
    columns with NaN - todrop
        _id
        name
        additional
        special
    list2.drop(columns=["_id", "name", "additional", "special])
    """

    ## dropping the columns? Yes
    # list2 = dropCols(list2, ["_id"])
    # list2.drop(columns=["Unnamed: 0", "Unnamed: 0.1", "Unnamed: 0.1.1"]) # weird - solution is above, from SO

    ## Types of cat vars for drinkType and establishment
    occurences = {}

    for col in ["drinkType", "establishmentType"]:
        occurences[col] = {}

        print("\nColumn: {}".format(col))
        alreadyNotedVars = []
        for a in list2[col]:
            if a not in alreadyNotedVars:
                alreadyNotedVars.append(a)
                n = list2[col].value_counts()[a]
                print("{} - {} occurences".format(a, n))
                occurences[col][a] = int(n)
    
    with open("variable_occurences_list2.json", "w", encoding="utf-8") as f:
        f.write(utils.json_beautify(occurences))
    catvar_occurences = """
        Column: drinkType
        [HOME-MADE] Milo Original - 13 occurences
        [CAN] Coca-cola/Pepsi Original - 20 occurences
        [BOTTLE] Coca-cola/Pepsi Original - 15 occurences
        [HOME-MADE] Bandung - 6 occurences
        [HOME-MADE] Lime Juice - 9 occurences
        [CAN] Sprite Original - 11 occurences
        [CAN] Fanta Grape/Orange - 8 occurences
        [BOTTLE] Sprite Original - 4 occurences
        [BOTTLE] Fanta Grape/Orange - 2 occurences

        Column: establishmentType
        Hawker - 10 occurences
        Convenience stall - 18 occurences
        Coffee shop - 23 occurences
        Supermarket - 10 occurences
        Mall - 11 occurences
        Vending - 4 occurences
        Hawker Centre - 4 occurences
        Vending machine - 1 occurences
        Vending Machine - 1 occurences
        Minimart - 4 occurences
        Store - 2 occurences
        """

    ## Handling the location coordinates
    # list2 = seperateCoords(list2)
    # list2 = list2.drop(columns=["location"])

    viewDf()

    ## output to new csv
    # list2.to_csv("list part 2 (MOD).csv", index=False)

    ### testing som matplotlib
    # testPlotLocations(list2)

def testPlot(df):
    """
    Just a test plot
    """
    x = np.array(df['lat'])
    y = np.array(df['price'])

    plt.title("Test") 
    plt.xlabel("Latitude") 
    plt.ylabel("Price/$") 
    plt.scatter(x, y, color ="red") 
    plt.show()

def testPlotLocations(df):
    """
    Might be useful to overlay a map as the bg image
    """
    x, y = np.array(df['long']), np.array(df['lat'])
    plt.title("Coordinates")
    plt.scatter(x, y)
    plt.show()

if __name__ == "__main__":
    main2()