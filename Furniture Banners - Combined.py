#!/usr/bin/env python
# coding: utf-8

## import
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import requests
from PIL import Image
import os
import glob
import pandas as pd
import duckdb
import fuckit
from googleapiclient.discovery import build
from google.oauth2 import service_account
import win32com.client
import time

## scrape

# init.
start_time = time.time()
outlook = win32com.client.Dispatch("outlook.application")

# pref.
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
options = webdriver.ChromeOptions().add_argument("ignore-certificate-errors")

# window
driver = webdriver.Chrome(options = options)
driver.maximize_window()

## Canadian Tire
def scrape_cdtr():

    # url
    url = "https://www.canadiantire.ca/en.html"
    driver.get(url)
    
    # soup
    soup_init = BeautifulSoup(driver.page_source, "html.parser")
    soup = soup_init.find("div", attrs = {"class": "regular slick-initialized slick-slider slick-dotted"}).find_all("img")
    len_soup = len(soup)
    
    # banners
    img_links = set()
    for s in soup: 
        b = s["src"]
        if "desktop" in b: img_links.add(b)
    
    # clear
    len_img = len(img_links)
    path = "C:/Users/shith/OneDrive/Banners by Stores/Canadian Tire/"
    files = glob.glob(path + "*")
    if len_img > 0: ret = [os.remove(f) for f in files]
    
    # save
    for i, link in enumerate(img_links):
        img_data = Image.open(requests.get(link, headers = headers, stream = True, verify = True).raw).convert("RGB")
        img_data.save(path + "cantire_" + str(i+1) + ".jpg", "JPEG")
    
    # record
    cdtr_df = pd.DataFrame()
    cdtr_df["banner_source"] = list(img_links)
    cdtr_df["platform"] = "Canadian Tire"
    cdtr_df["platform_link"] = url
    
    # return
    return cdtr_df

## Costco
def scrape_cost():

    # url
    url = "https://www.costco.ca/"
    driver.get(url)
    
    # soup
    soup_init = BeautifulSoup(driver.page_source, "html.parser")
    soup = soup_init.find("div", attrs = {"class": "slick-list draggable"}).find_all("img")
    
    # banners
    img_links = set()
    for s in soup: 
        b = s["data-src"]
        if "d-hero" in b: img_links.add(b)
    
    # clear
    len_img = len(img_links)
    path = "C:/Users/shith/OneDrive/Banners by Stores/Costco/"
    files = glob.glob(path + "*")
    if len_img > 0: ret = [os.remove(f) for f in files]
    
    # save
    for i, link in enumerate(img_links):
        img_data = Image.open(requests.get(link, headers = headers, stream = True, verify = True).raw).convert("RGB")
        img_data.save(path + "costco_" + str(i+1) + ".jpg", "JPEG")
    
    # record
    cost_df = pd.DataFrame()
    cost_df["banner_source"] = list(img_links)
    cost_df["platform"] = "Costco"
    cost_df["platform_link"] = url

    # return
    return cost_df

## Wayfair
def scrape_wafr():

    # url
    url = "https://www.wayfair.com/"
    driver.get(url)
    
    # soup
    soup_init = BeautifulSoup(driver.page_source, "html.parser")
    soup = soup_init.find("div", attrs = {"data-test-id": re.compile(".*arousel.*")}).find_all("img")

    # banners
    img_links = set()
    for s in soup: img_links.add(s["src"])
    
    # clear
    len_img = len(img_links)
    path = "C:/Users/shith/OneDrive/Banners by Stores/Wayfair/"
    files = glob.glob(path + "*")
    if len_img > 0: ret = [os.remove(f) for f in files]
    
    # save
    for i, link in enumerate(img_links):
        img_data = Image.open(requests.get(link, headers = headers, stream = True, verify = True).raw).convert("RGB")
        img_data.save(path + "wafr_" + str(i+1) + ".jpg", "JPEG")
    
    # record
    wafr_df = pd.DataFrame()
    wafr_df["banner_source"] = list(img_links)
    wafr_df["platform"] = "Wayfair"
    wafr_df["platform_link"] = url
    
    # return
    return wafr_df

## SportChek
def scrape_schk():

    # url
    url = "https://www.sportchek.ca/en.html"
    driver.get(url)
    
    # soup
    soup_init = BeautifulSoup(driver.page_source, "html.parser")
    soup = soup_init.find("div", attrs = {"class": "aspotCarousel aem-GridColumn aem-GridColumn--default--12"}).find_all("img")
    
    # banners
    img_links = set()
    for s in soup:
        b = s["src"]
        if "-desktop" in b: img_links.add(b)
    
    # clear
    len_img = len(img_links)
    path = "C:/Users/shith/OneDrive/Banners by Stores/SportChek/"
    files = glob.glob(path + "*")
    if len_img > 0: ret = [os.remove(f) for f in files]
    
    # save
    for i, link in enumerate(img_links):
        img_data = Image.open(requests.get(link, headers = headers, stream = True, verify = True).raw).convert("RGB")
        img_data.save(path + "schek_" + str(i+1) + ".jpg", "JPEG")
    
    # record
    schk_df = pd.DataFrame()
    schk_df["banner_source"] = list(img_links)
    schk_df["platform"] = "SportChek"
    schk_df["platform_link"] = url

    # return
    return schk_df

## Rona
def scrape_rona():

    # url
    url = "https://www.rona.ca/en"
    driver.get(url)
    
    # soup
    soup_init = BeautifulSoup(driver.page_source, "html.parser")
    soup = soup_init.find("div", attrs = {"class": "row row--flex"}).find_all("img")
    
    # banners
    img_links = list()
    for s in soup: 
        b = "https://www.rona.ca" + s["src"]
        if "banner" in b: img_links.append(b)
    
    # clear
    len_img = len(img_links)
    path = "C:/Users/shith/OneDrive/Banners by Stores/Rona/"
    files = glob.glob(path + "*")
    if len_img > 0: ret = [os.remove(f) for f in files]
    
    # save
    for i, link in enumerate(img_links):
        img_data = Image.open(requests.get(link, headers = headers, stream = True, verify = True).raw).convert("RGB")
        img_data.save(path + "rona_" + str(i+1) + ".jpg", "JPEG")
    
    # record
    rona_df = pd.DataFrame()
    rona_df["banner_source"] = list(img_links)
    rona_df["platform"] = "Rona"
    rona_df["platform_link"] = url

    # return
    return rona_df

## Lowe's
def scrape_lows():

    # url
    url = "https://www.lowes.com/"
    driver.get(url)
    
    # soup
    soup_init = BeautifulSoup(driver.page_source, "html.parser")
    soup1 = soup_init.find("div", attrs = {"data-bannertype": "GAMHeroBannerCarousel"}).find_all("source", attrs = {"type": "image/jpeg"})
    soup2 = soup_init.find("div", attrs = {"data-bannertype": "GAMHeroBannerCarousel"}).find_all("img")
    
    # banners
    img_links = set()
    for s in soup1: 
        b = s["srcset"]
        if "-mow" not in b and "-tab" not in b: img_links.add(b)
    for s in soup2: 
        b = s["src"]
        if "-dt" in b: img_links.add(b)
    
    # clear
    len_img = len(img_links)
    path = "C:/Users/shith/OneDrive/Banners by Stores/Lowe's/"
    files = glob.glob(path + "*")
    if len_img > 0: ret = [os.remove(f) for f in files]
    
    # save
    for i, link in enumerate(img_links):
        img_data = Image.open(requests.get(link, headers = headers, stream = True, verify = True).raw).convert("RGB")
        img_data.save(path + "lowes_" + str(i+1) + ".jpg", "JPEG")
    
    # record
    lows_df = pd.DataFrame()
    lows_df["banner_source"] = list(img_links)
    lows_df["platform"] = "Lowes"
    lows_df["platform_link"] = url

    # retutn
    return lows_df

## Sleepcountry
def scrape_sleep():

    # url
    url = "https://www.sleepcountry.ca/"
    driver.get(url)
    
    # delay
    time.sleep(5)
    
    # soup
    soup_init = BeautifulSoup(driver.page_source, "html.parser")
    soup = soup_init.find("div", attrs = {"class": "slick-track"}).find_all("img")
    
    # banners
    img_links = set()
    for s in soup: 
        try: b = ("https://www.sleepcountry.ca" + s["src"]).replace(" ", "%20")
        except: continue
        if "mobile" not in b.lower(): img_links.add(b)
    
    # clear
    len_img = len(img_links)
    path = "C:/Users/shith/OneDrive/Banners by Stores/Sleep Country/"
    files = glob.glob(path + "*")
    if len_img > 0: ret = [os.remove(f) for f in files]
    
    # save
    for i, link in enumerate(img_links):
        try: # non-svg
            img_data = Image.open(requests.get(link, headers = headers, stream = True, verify = True).raw).convert("RGB")
            img_data.save(path + "sleep_" + str(i+1) + ".jpg", "JPEG")
        except: # svg
            img_data = requests.get(link).text
            with open(path + "sleep_" + str(i+1) + ".svg", "w") as file: file.write(img_data)
    
    # record
    sleep_df = pd.DataFrame()
    sleep_df["banner_source"] = list(img_links)
    sleep_df["platform"] = "Sleep Country"
    sleep_df["platform_link"] = url

    # return
    return sleep_df

## caller
@fuckit
def scrape_call():

    # call
    ecom_df = pd.DataFrame()
    ecom_df = pd.concat([ecom_df, scrape_cdtr()], ignore_index = True)
    ecom_df = pd.concat([ecom_df, scrape_wafr()], ignore_index = True)
    ecom_df = pd.concat([ecom_df, scrape_schk()], ignore_index = True)
    ecom_df = pd.concat([ecom_df, scrape_rona()], ignore_index = True)
    ecom_df = pd.concat([ecom_df, scrape_lows()], ignore_index = True)
    ecom_df = pd.concat([ecom_df, scrape_cost()], ignore_index = True)
    ecom_df = pd.concat([ecom_df,scrape_sleep()], ignore_index = True)

    # error
    to_scraped = set(["Canadian Tire", "Wayfair", "SportChek", "Rona", "Lowes", "Sleep Country", "Costco"])
    is_scraped = set(duckdb.query('''select platform from ecom_df''').df()["platform"].tolist())
    err_scrape = to_scraped - is_scraped
    
    # report
    newmail = outlook.CreateItem(0x0)
    newmail.Subject = "Banner Errors (" + str(len(err_scrape)) + ")"
    newmail.HTMLbody = "Banner websites to throw error are: " + str(err_scrape)
    newmail.To = "shithi30@outlook.com"
    newmail.Send()

    # return
    return ecom_df

## services

# creds
SERVICE_ACCOUNT_FILE = "read-write-to-gsheet-apis-1-04f16c652b1e.json"
SAMPLE_SPREADSHEET_ID = "1rvnYmn4-6T37GqeUFbRieY2uGYu8qg8ng62YGDjoc8M"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# APIs
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes = SCOPES)
service = build("sheets", "v4", credentials = creds)
sheet = service.spreadsheets()

## ETL

# extract
values = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range = "Competitor Banners!B1:F").execute().get("values", [])
prev_df = pd.DataFrame(values[1:] , columns = values[0])

# transform - all
pres_df = scrape_call()
qry = '''
-- old
select banner_source, platform, platform_link, 0 if_new, report_time from prev_df union
-- new
select banner_source, platform, platform_link, 1 if_new, strftime(now(), '%d-%b-%y, %I:%M %p') report_time
from pres_df
where banner_source not in(select banner_source from prev_df)
'''
pres_df = duckdb.query(qry).df()

# load
sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range= "Competitor Banners!B1:F").execute()
sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range = "Competitor Banners!B1", valueInputOption = "USER_ENTERED", body = {"values": [pres_df.columns.values.tolist()] + pres_df.fillna("").values.tolist()}).execute()

## new

# new banners
new_br_df = duckdb.query('''select * from pres_df where if_new=1''').df()
new_pltfm = new_br_df["platform"].tolist()
new_links = new_br_df["banner_source"].tolist()
len_links = len(new_links)

# clear
path = "C:/Users/shith/OneDrive/Banners by Stores/New/"
files = glob.glob(path + "*")
if len_links > 0: ret = [os.remove(f) for f in files]

# save
for i in range(0, len_links): 
    img_link = new_links[i]
    try: # non-svg
        img_data = Image.open(requests.get(img_link, headers = headers, stream = True, verify = True).raw).convert("RGB")
        img_data.save(path + "new_" + str(i+1) + "_" + new_pltfm[i] + ".jpg", "JPEG")
    except: # svg
        img_data = requests.get(img_link).text
        with open(path + "new_" + str(i+1) + "_" + new_pltfm[i] + ".svg", "w") as file: file.write(img_data)

## email

# object
newmail = outlook.CreateItem(0x0)

# subject
newmail.Subject = "New Furniture Banners (" + str(len_links) + "*)" if len_links > 0 else "New Furniture Banners"

# expressions, ref: https://www.w3schools.com/charsets/ref_emoji.asp
emos = [128194, 128680, 128203, 128345] # folders, alarm, list, clock

# body
newmail.HTMLbody = '''
Dear concern,<br>
<br>
Please click to find:<br>
''' + "&#" + str(emos[0]) + ''' Store-wise banners, <a href="https://1drv.ms/f/s!AnD8IACnC-3ygax02IKcjdsG-VcF9w?e=GYAam2"> here.</a><br>
''' + "&#" + str(emos[1]) + ''' New banners <b>(''' + str(len_links) + ''')</b>, <a href="https://1drv.ms/f/s!AnD8IACnC-3yga4ff6P0d690TeyBcA?e=PAmSuW"> here</a> (attached).<br>
''' + "&#" + str(emos[2]) + '''  Full, historical list of all banners, <a href="https://docs.google.com/spreadsheets/d/1rvnYmn4-6T37GqeUFbRieY2uGYu8qg8ng62YGDjoc8M/edit?usp=sharing"> here.</a><br>
''' + "&#" + str(emos[3]) + ''' Elapsed time to scrape (sec): ''' + str(round(time.time() - start_time)) + '''<br>
<br>
Thanks,<br>
Shithi Maitra<br>
Asst. Manager, CS Analytics<br>
Unilever BD Ltd.<br>
'''

# attach
path = "C:/Users/shith/OneDrive/Banners by Stores/New/"
files = glob.glob(path + "*")
for f in files: ret = newmail.Attachments.Add(f) if len_links > 0 else None

# send
newmail.To = "shithi30@outlook.com"
newmail.Send()

## end
driver.close()





