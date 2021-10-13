import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.ticker import StrMethodFormatter
import pandas as pd

import utils
import re
import json

MRTStations = {
    "Ang Mo Kio": (1.370017, 103.84945),
    "Marymount": (1.349167, 103.839444),
    "Bishan": (1.351111, 103.848333)
}

def calculateDistance(coord1, coord2): # in km
    return np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) * 111

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

def dealingWithCatVars():
    """
    This imports the json and seems how to deal with the cat vars.

    """
    threshold = 0.8
    catnumber = 5

    with open("variable_occurences_list2.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    """
    Modifying the cat vars - some errors in data input
    For establishmentType
    Hawker -> Hawker Centre
    Vending machine, Vending -> Vending Machine
    """

    newEst = {}
    for a in list(data["establishmentType"]):
        if a == "Hawker":
            try: 
                newEst["Hawker Centre"] += data["establishmentType"][a]
            except:
                newEst["Hawker Centre"] = data["establishmentType"][a]
        elif a == "Vending machine" or a == "Vending":
            try:
                newEst["Vending Machine"] += data["establishmentType"][a]
            except:
                newEst["Vending Machine"] = data["establishmentType"][a]
        else:
            try:
                newEst[a] += data["establishmentType"][a]
            except:
                newEst[a] = data["establishmentType"][a]


    data["establishmentType"] = newEst
    # print(utils.json_beautify(data))

    for col in list(data):
        vars = dict(sorted(data[col].items(), key=lambda x:x[1]))  # dict - sorted
        total = sum(vars.values())
        # print("TOTAL: {}".format(total))

        Ctotal = 0
        varsToCare = []
        varsToIgnore = []
        for var in list(vars):
            Ctotal += vars[var]
            if ( total - Ctotal ) / total < threshold:
                varsToCare.append(var)
            else:
                varsToIgnore.append(var)

        print(varsToIgnore, varsToCare)

def distToMrt(df):
    df["distance to AMK"] = df.apply(lambda x: calculateDistance(
        (x["lat"], x["long"]),
        MRTStations["Ang Mo Kio"]
    ), axis = 1)

    df["distance to Bishan"] = df.apply(lambda x: calculateDistance(
        (x["lat"], x["long"]),
        MRTStations["Bishan"]
    ), axis = 1)

    df["distance to Marymount"] = df.apply(lambda x: calculateDistance(
        (x["lat"], x["long"]),
        MRTStations["Marymount"]
    ), axis = 1)

    df["shortest distance"] = df.apply(lambda x: min([
        x["distance to AMK"],
        x["distance to Bishan"],
        x["distance to Marymount"]
    ]), axis = 1)

    return df

def catVar(df):

    ## dealing with the repeated variables first
    # for EstType
    df.loc[df['establishmentType'] == "Hawker", 'establishmentType'] = "Hawker Centre"
    df.loc[df['establishmentType'].isin(["Vending machine", "Vending"]), 'establishmentType'] = "Vending Machine"

    ## then this
    drinkTypeCats = {
        "[BOTTLE] Coca-cola/Pepsi Original": 6,
        "[BOTTLE] Fanta Grape/Orange": 8,
        "[BOTTLE] Sprite Original": 8,
        "[CAN] Coca-cola/Pepsi Original": 7,
        "[CAN] Fanta Grape/Orange": 1,
        "[CAN] Sprite Original": 3,
        "[HOME-MADE] Bandung": 8,
        "[HOME-MADE] Lime Juice": 2,
        "[HOME-MADE] Milo Original": 4
    } # alternatively bottles vs can vs homemade - wait lest not deal with this yet
    estTypeCats = {
        "Coffee shop": 5,
        "Convenience stall": 4,
        "Hawker Centre": 3,
        "Mall": 2,
        "Minimart": 6,
        "Store": 6,
        "Supermarket": 1,
        "Vending Machine": 6
    } # 6 becomes "other"

    for cat in list(estTypeCats):
        val = estTypeCats[cat]

        df.loc[df['establishmentType'] == cat, "estTypeInt"] = int(val)

    ## yay !

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
    # Exports to a Json
    # occurences = {}

    # for col in ["drinkType", "establishmentType"]:
    #     occurences[col] = {}

    #     print("\nColumn: {}".format(col))
    #     alreadyNotedVars = []
    #     for a in list2[col]:
    #         if a not in alreadyNotedVars:
    #             alreadyNotedVars.append(a)
    #             n = list2[col].value_counts()[a]
    #             print("{} - {} occurences".format(a, n))
    #             occurences[col][a] = int(n)
    
    # with open("variable_occurences_list2.json", "w", encoding="utf-8") as f:
    #     f.write(utils.json_beautify(occurences))
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

    ## Dealing with the categorical variables
    list2 = catVar(list2)

    ## distances and shit
    list2 = distToMrt(list2)

    # viewDf()

    ## output to new csv
    # list2.to_csv("list part 2 (MOD).csv", index=False)

    ### testing som matplotlib
    # testPlotLocations(list2)
    
    plots(list2)

def plots(df):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    ax1 = testPlotLocations(df, ax1)
    ax2 = plotEstType(df, ax2)
    ax3 = plotDistToMrts(df, ax3)

    plt.show()

def plotEstType(df, ax):
    ## DONE

    labels = ['Supermarket', 'Mall', 'Hawker Centre', 'Convenience stall', 'Coffee shop', 'Other'] # 6 
    means = []
    std = []
    maxs = []
    mins = []
    for n in range(1,7):
        means.append(df.loc[df["estTypeInt"] == n]["price"].mean())
        maxs.append(df.loc[df["estTypeInt"] == n]["price"].max())
        mins.append(df.loc[df["estTypeInt"] == n]["price"].min())

    x = np.arange(len(labels))
    width = 0.2

    ax.set_title("Price Based on Type of Establishment") 
    ax.set_ylabel("Price/$") 

    ax.set_xticks(x)
    ax.set_xticklabels(labels)

    bars = ax.bar(labels, means, width, yerr=[
        np.array(means) - np.array(mins), 
        np.array(maxs) - np.array(means)],
        label='Establishments')

    ax.bar_label(bars)

    return ax

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

def testPlotLocations(df, ax):
    """
    Might be useful to overlay a map as the bg image
    """
    s = 5

    x, y = np.array(df['long']), np.array(df['lat'])
    NSLy, NSLx = [MRTStations["Bishan"][0], MRTStations["Ang Mo Kio"][0]], [MRTStations["Bishan"][1], MRTStations["Ang Mo Kio"][1]]
    CCLy, CCLx = [MRTStations["Marymount"][0]], [MRTStations["Marymount"][1]]
    ax.set_title("Locations")
    ax.imshow(plt.imread("map.png"), extent=[103.8293, 103.85097, 1.3446, 1.37439], alpha=0.7)
    ax.scatter(x, y, s=s, color="black")
    ax.set_aspect('equal')
    ax.scatter(CCLx, CCLy, color = "yellow", s=s)
    ax.scatter(NSLx, NSLy, color = "red", s=s)
    ax.grid(linewidth='0.3')

    return ax

def plotDistToMrts(df, ax):

    prices = df['price']
    dist = df["shortest distance"]

    ax.set_title("Prices based on the Shortest Distance to an MRT Station") 
    ax.set_xlabel("Shortest Distance to an MRT Station/km") 
    ax.set_ylabel("Price/$") 
    ax.set_xticks(np.arange(0, max(dist) + 1, 0.2))
    ax.set_yticks(np.arange(0, max(prices) + 1, 0.5))
    ax.grid(linewidth='0.3')
    ax.scatter(dist, prices, s=8, alpha=.75) 

    return ax

if __name__ == "__main__":
    main2()