# Import Statements
import pandas as pd
import numpy as np

# Importing Data
def import_data():

    SHEET_ID = '1BH_B_Df_7e2l6AH8_8a0aK70nlAJXfCTwfyCgxkL5C8'
    SHEET_NAME = 'cdr.fyi_raw'
    SHEET_NAME1 = 'Main sheet (merged with cdr.fyi)'
    SHEET_NAME2 = 'List of revisions'
    url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    cdr_fyi = pd.read_csv(url, decimal=",")

    cdr_fyi["Total price (USD)"] = cdr_fyi["Total price (USD)"].replace(0.0, np.nan)
    cdr_fyi["Price per Ton"] = cdr_fyi["Total price (USD)"] / cdr_fyi["Tons Purchased"]
    cdr_fyi["Announcement Date"] = cdr_fyi["Announcement Date"].str.split(" ", n=1).str[0]
    cdr_fyi.rename(columns={"Tons Purchased": "Tons Purchased/Sold"}, inplace=True)
    cdr_fyi["CDR Method"] = np.where(cdr_fyi["CDR Method"] == "Enhanced Weathering", "Enhanced weathering", cdr_fyi["CDR Method"])

    return cdr_fyi
