#!/usr/bin/env python
# coding: utf-8

## import
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import duckdb
from googleapiclient.discovery import build
from google.oauth2 import service_account

## data

# orgs.
companies = ["Canadian Tire", "Leon's", "Wayfair", "Lowe's", "COSTCO", "Amazon", "Walmart"]
tickers = ["CTC.TO", "LNF.TO", "W", "LOW", "COST", "AMZN", "WMT"]

# timeframe
end_date = datetime.today()
start_date = end_date - timedelta(days = 60)

# stock data - closing price
close_df = pd.DataFrame()
for ticker in tickers:
    df = yf.download(ticker, start = start_date, end = end_date)
    close_df[ticker] = df["Close"]

# stock data - refine cols
close_df = close_df.reset_index()
close_df.columns = ["Stock Closing Date"] + ["Price - " + t for t in companies]
close_df["Stock Closing Date"] = close_df["Stock Closing Date"].astype(str)

# fluctuations
qry = '''
select 
    *,
    ("Price - Canadian Tire" - lag("Price - Canadian Tire") OVER (ORDER BY "Stock Closing Date")) / lag("Price - Canadian Tire") OVER (ORDER BY "Stock Closing Date") "Fluct.% - Canadian Tire",   
    ("Price - Leon's" - lag("Price - Leon's") OVER (ORDER BY "Stock Closing Date")) / lag("Price - Leon's") OVER (ORDER BY "Stock Closing Date") "Fluct.% - Leon's",
    ("Price - Wayfair" - lag("Price - Wayfair") OVER (ORDER BY "Stock Closing Date")) / lag("Price - Wayfair") OVER (ORDER BY "Stock Closing Date") "Fluct.% - Wayfair",
    ("Price - Lowe's" - lag("Price - Lowe's") OVER (ORDER BY "Stock Closing Date")) / lag("Price - Lowe's") OVER (ORDER BY "Stock Closing Date") "Fluct.% - Lowe's",
    ("Price - COSTCO" - lag("Price - COSTCO") OVER (ORDER BY "Stock Closing Date")) / lag("Price - COSTCO") OVER (ORDER BY "Stock Closing Date") "Fluct.% - COSTCO",
    ("Price - Amazon" - lag("Price - Amazon") OVER (ORDER BY "Stock Closing Date")) / lag("Price - Amazon") OVER (ORDER BY "Stock Closing Date") "Fluct.% - Amazon",
    ("Price - Walmart" - lag("Price - Walmart") OVER (ORDER BY "Stock Closing Date")) / lag("Price - Walmart") OVER (ORDER BY "Stock Closing Date") "Fluct.% - Walmart"
from close_df
'''
fluct_df = duckdb.query(qry).df()

## ETL

# creds
SERVICE_ACCOUNT_FILE = "read-write-to-gsheet-apis-1-04f16c652b1e.json"
SAMPLE_SPREADSHEET_ID = "1rvnYmn4-6T37GqeUFbRieY2uGYu8qg8ng62YGDjoc8M"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# APIs
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes = SCOPES)
service = build("sheets", "v4", credentials = creds)
sheet = service.spreadsheets()

# update 
clear = sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Furniture - Stocks").execute()
reqst = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="'Furniture - Stocks'!A1", valueInputOption="USER_ENTERED", body={"values": [fluct_df.columns.values.tolist()] + fluct_df.fillna("").values.tolist()}).execute()



