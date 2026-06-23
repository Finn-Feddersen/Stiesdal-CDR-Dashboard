# Import Statements
import pandas as pd
import numpy as np
import os

# Importing Data
def import_data():

    DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cdr_fyi_raw.csv")
    cdr_fyi = pd.read_csv(DATA_PATH, decimal=",")
    
    cdr_fyi["Total price (USD)"] = cdr_fyi["Total price (USD)"].replace(0.0, np.nan)
    cdr_fyi["Price per Ton"] = cdr_fyi["Total price (USD)"] / cdr_fyi["Tons Purchased"]
    cdr_fyi["Announcement Date"] = cdr_fyi["Announcement Date"].str.split(" ", n=1).str[0]
    cdr_fyi.rename(columns={"Tons Purchased": "Tons Purchased/Sold"}, inplace=True)
    cdr_fyi["CDR Method"] = np.where(cdr_fyi["CDR Method"] == "Enhanced Weathering", "Enhanced weathering", cdr_fyi["CDR Method"])

    return cdr_fyi
