#!/usr/bin/env python
# coding: utf-8

## import
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import duckdb
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
import smtplib
from email.mime.text import MIMEText
from pretty_html_table import build_table

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
SERVICE_ACCOUNT_FILE = json.loads(os.getenv("READ_WRITE_TO_GSHEET_APIS_JSON"))
SAMPLE_SPREADSHEET_ID = "1rvnYmn4-6T37GqeUFbRieY2uGYu8qg8ng62YGDjoc8M"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# APIs
creds = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes = SCOPES)
service = build("sheets", "v4", credentials = creds)
sheet = service.spreadsheets()

# update 
clear = sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Furniture - Stocks").execute()
reqst = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="'Furniture - Stocks'!A1", valueInputOption="USER_ENTERED", body={"values": [fluct_df.columns.values.tolist()] + fluct_df.fillna("").values.tolist()}).execute()

## summary
qry = '''
select 
    "Stock Closing Date",
    concat(round("Fluct.% - Canadian Tire" * 100, 2), '%') "Fluct.% - Canadian Tire",
    concat(round("Fluct.% - Leon's" * 100, 2), '%') "Fluct.% - Leon's",
    concat(round("Fluct.% - Wayfair" * 100, 2), '%') "Fluct.% - Wayfair",
    concat(round("Fluct.% - Lowe's" * 100, 2), '%') "Fluct.% - Lowe's",
    concat(round("Fluct.% - COSTCO" * 100, 2), '%') "Fluct.% - COSTCO",
    concat(round("Fluct.% - Amazon" * 100, 2), '%') "Fluct.% - Amazon",
    concat(round("Fluct.% - Walmart" * 100, 2), '%') "Fluct.% - Walmart"
from fluct_df
order by 1 desc
limit 1
'''
summ_df = duckdb.query(qry).df()

## email

# from, to, body
sender_email = "shithi30@gmail.com"
recivr_email = ["shithi30@outlook.com"]
body = '''
Dear concern,<br><br>
Summarized below are, today's Furniture Stock Market Price fluctuations. Recent trends can be found <a href="https://docs.google.com/spreadsheets/d/1rvnYmn4-6T37GqeUFbRieY2uGYu8qg8ng62YGDjoc8M/edit?gid=217963277#gid=217963277">here</a>.
''' + build_table(summ_df, "green_light", font_size="12px", text_align="left") + '''
Note, the data presented reflects statistics when <i>yfinance</i> API was called. This is an auto. email via <i>Smtplib</i>.<br><br>
Thanks,<br>
Shithi Maitra<br>
Ex Asst. Manager, CSE<br>
Unilever BD Ltd.<br>
'''

# object
html_msg = MIMEText(body, "html")
html_msg["Subject"] = "Furniture Stock Prc. - Daily"
html_msg["From"] = "Shithi Maitra"
html_msg["To"] = ", ".join(recivr_email)

# send
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
   server.login(sender_email, "uhfu cppa sxgh bwpr")
   server.sendmail(sender_email, recivr_email, html_msg.as_string())



