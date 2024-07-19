#!/usr/bin/env python
# coding: utf-8

# In[1]:


## import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import re
import pandas as pd
import duckdb
import time
import fuckit
import warnings
import win32com.client
from googleapiclient.discovery import build
from google.oauth2 import service_account


# In[2]:


## scrape

# init.
start_time = time.time()
outlook = win32com.client.Dispatch("outlook.application")

# window
driver = webdriver.Chrome()
driver.maximize_window()

# pref.
driver.implicitly_wait(30)
warnings.filterwarnings("ignore")
pd.set_option("display.max_rows", 3000)


# In[3]:


## parse
def parse_flyer(site, offers, url):
    
    # item
    flyer_df = pd.DataFrame(columns = ["flyer_item", "sku", "offer", "discount", "offer_price", "instalment_mth", "platform", "url"])
    for offer in offers:  
        flyer_item = offer
    
        # seperate
        offer = offer[:-22].split(", ")
        sku = offer[0]
        discount_offer = ", ".join(offer[1:-1])
        price_instalment = offer[-1]

        # price + instalment
        pattern = re.compile("\$[0-9\.]+")
        vals = pattern.findall(price_instalment)
        # price
        try: price = vals[0][1:]
        except: price = None
        # instalment
        try: instalment = vals[1][1:]
        except: instalment = None

        # discount - dollar
        pattern = re.compile("\$[0-9\.]+")
        try: 
            val = pattern.findall(discount_offer)[0]
            discount = val[1:]
        except: discount = None
        # discount - cent
        pattern = re.compile("[0-9\.]+¢")
        try: 
            val = pattern.findall(discount_offer)[0]
            discount = str(float(val[:-1]) / 100)
        except: discount = None if discount is None else discount
        # discount - percent
        pattern = re.compile("[0-9\.]+%")
        try: 
            val = pattern.findall(discount_offer)[0]
            discount = str((float(price)*100) / (100 - float(val[:-1])) - float(price))
        except: discount = None if discount is None else discount

        # append
        flyer_df = pd.concat([pd.DataFrame([[flyer_item, sku, discount_offer, discount, price, instalment, site, url]], columns = flyer_df.columns), flyer_df], ignore_index = True)
    
    # refine
    qry = '''
    select 
        flyer_item, sku, offer, 
        discount::numeric discount, offer_price::numeric offer_price, discount::numeric+offer_price::numeric regular_price, instalment_mth::numeric instalment_mth, 
        platform, url, strftime(now(), '%Y-%m-%d, %I:%M %p') report_time
    from flyer_df
    '''
    flyer_df = duckdb.query(qry).df()
    
    # show
    return flyer_df


# In[4]:


## Leon's
def scrape_leons():

    # url
    url = "https://www.leons.ca/pages/flyer"
    driver.get(url)
    
    # postcode
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='Information Panel']"))
    elem = driver.find_element(By.ID, "postal-input")
    elem.clear()
    elem.send_keys("N8W1J2\n")
    
    # outlet
    elem = driver.find_elements(By.CLASS_NAME, "select")
    elem[0].click()
    
    # cross
    driver.switch_to.default_content()
    elem = driver.find_element(By.CLASS_NAME, "ltkpopup-close")
    elem.click()
    
    # soup
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@class='flippiframe mainframe']"))
    soup = BeautifulSoup(driver.page_source, "html.parser").find("div", attrs = {"class": "sfml-wrapper"}).find_all("button")
    
    # data
    offers = []
    for s in soup:
        try: offer = s["aria-label"]
        except: continue
        if offer not in offers: offers.append(offer)

    # return
    return parse_flyer("Leon's", offers, url)


# In[5]:


## The Brick
def scrape_thebrick():
    
    # url
    url = "https://www.thebrick.com/pages/flyer"
    driver.get(url)
    
    # soup
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='Main Panel']"))
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser").find("sfml-linear-layout").find_all("button")
    
    # data
    offers = []
    for s in soup:
        try: offer = s["aria-label"]
        except: continue
        if offer not in offers: offers.append(offer)
            
    # return
    return parse_flyer("The Brick", offers, url)


# In[6]:


## Tepperman's
def scrape_teppermans():

    # url
    url = "https://www.teppermans.com/flyers"
    driver.get(url)
    
    # cross
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@referrerpolicy='origin']"))
    driver.find_element(By.ID, "closeIconContainer").click()
    driver.switch_to.default_content()
    
    # soup
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@class='flippiframe mainframe']"))
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser").find("sfml-linear-layout").find_all("button")
    
    # data
    offers = []
    for s in soup:
        try: offer = s["aria-label"]
        except: continue
        if offer not in offers: offers.append(offer)

    # return
    return parse_flyer("Tepperman's", offers, url)


# In[7]:


## Walmart
def scrape_walmart():

    # url
    url = "https://www.walmart.ca/en/flyer"
    driver.get(url)
    
    # navigate
    time.sleep(5)
    element = driver.find_element(By.CSS_SELECTOR, "#px-captcha")
    
    # long press (captcha: https://stackoverflow.com/questions/68636955)
    action = ActionChains(driver)
    action.click_and_hold(element)
    action.perform()
    time.sleep(10)
    
    # release
    action.release(element)
    action.perform()
    
    # cross
    elem = driver.find_element(By.XPATH, ".//button[@aria-label='Close dialogue']")
    elem.send_keys("\n")
    
    # soup
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@class='flippiframe mainframe']"))
    soup = BeautifulSoup(driver.page_source, "html.parser").find("div", attrs = {"class": "sfml-wrapper"}).find_all("button")
    
    # data
    offers = []
    for s in soup:
        try: offer = s["aria-label"]
        except: continue
        if offer not in offers: offers.append(offer)

    # retrieve, refine, return
    flyer_df = parse_flyer("Walmart", offers, url)
    flyer_df["instalment_mth"] = None
    return flyer_df


# In[8]:


## caller
@fuckit
def scrape_call():

    # call
    flyer_df = pd.DataFrame()
    flyer_df = pd.concat([flyer_df, scrape_thebrick()], ignore_index = True)
    flyer_df = pd.concat([flyer_df, scrape_teppermans()], ignore_index = True)
    flyer_df = pd.concat([flyer_df, scrape_leons()], ignore_index = True)
    flyer_df = pd.concat([flyer_df, scrape_walmart()], ignore_index = True)

    # error
    to_scraped = set(["The Brick", "Tepperman's", "Leon's", "Walmart"])
    is_scraped = set(duckdb.query('''select platform from flyer_df''').df()["platform"].tolist())
    err_scrape = to_scraped - is_scraped
    
    # report
    newmail = outlook.CreateItem(0x0)
    newmail.Subject = "Flyer Errors (" + str(len(err_scrape)) + ")"
    newmail.HTMLbody = "Flyer websites to throw error are: " + str(err_scrape)
    newmail.To = "shithi30@outlook.com"
    newmail.Send()

    # return
    return flyer_df


# In[9]:


## services

# creds
SERVICE_ACCOUNT_FILE = "read-write-to-gsheet-apis-1-04f16c652b1e.json"
SAMPLE_SPREADSHEET_ID = "1rvnYmn4-6T37GqeUFbRieY2uGYu8qg8ng62YGDjoc8M"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# APIs
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes = SCOPES)
service = build("sheets", "v4", credentials = creds)
sheet = service.spreadsheets()


# In[10]:


## ETL extract
extract_df = scrape_call()


# In[11]:


## ETL transform - categorize

# classify
def classify_item(keys, item, cat, cat_init):
    if cat_init is not None: return cat_init
    for key in keys: 
        if key in item: return cat
            
# init./iter.
flyer_cat = []
iterator = extract_df.iterrows()
for index, row in iterator:
    item, cat = row["flyer_item"].lower(), None

    # label
    cat = classify_item(["mattress", " bed", "comforter", "pillow", "bedroom", "duvet", "adjustable base", "sheet set"], item, "Bedroom & Mattress", cat)
    cat = classify_item(["reclin", "sofa", "loveseat", "sectional", "ottoman", "daybed"], item, "Sofa Sets", cat)
    cat = classify_item(["tv", "lamp"], item, "TV & Lighting", cat)
    cat = classify_item([" table", "chair", "desk", "stool"], item, "Table+Chair+Desk", cat)
    cat = classify_item(["dining", "convection", "microwave", "bbq", "induction", "fry", "oven", "gas"], item, "BBQ, Cooking & Dining", cat)
    cat = classify_item(["fridge", "freezer", "refrigerator", "air conditioner", " ice maker", "ice cream"], item, "Refrigeration", cat)
    cat = classify_item(["washer", "dryer", "dishwasher"], item, "Cleaning & Drying", cat)
    flyer_cat.append(cat)
    
# assign
extract_df["flyer_cat"] = flyer_cat


# In[12]:


## ETL transform - flyer
flyer_df = duckdb.query('''select flyer_item, sku, concat('=TO_TEXT("', replace(offer, '"', '""'), '")') offer, discount, offer_price, regular_price, instalment_mth, platform, flyer_cat category, url, report_time from extract_df''').df()


# In[13]:


## ETL transform - platform
qry = '''
select
    platform,
    -- count
    count(flyer_item) "flyer items",
    count(case when offer!='' then flyer_item else null end) "offer items",
    count(case when discount is not null then flyer_item else null end) "discount items",
    count(case when instalment_mth is not null then flyer_item else null end) "items by instl./mth",
    -- ratio
    count(case when offer!='' then flyer_item else null end)*1.00 / count(flyer_item) "offer items %",
    count(case when discount is not null then flyer_item else null end) / count(flyer_item) "discount items %",
    sum(discount) / sum(case when discount is not null then regular_price else null end) "avg. discount %",
    sum(instalment_mth) / sum(case when instalment_mth is not null then offer_price else null end) "avg. instl./mth %"
from extract_df
group by 1
'''
sumry_df = duckdb.query(qry).df()


# In[14]:


# ETL transform - category
qry = '''
select
    flyer_cat "flyer - category",
    -- count
    count(flyer_item) "flyer items",
    count(case when offer!='' then flyer_item else null end) "offer items",
    count(case when discount is not null then flyer_item else null end) "discount items",
    count(case when instalment_mth is not null then flyer_item else null end) "items by instl./mth",
    -- ratio
    count(flyer_item)*1.00 / (select count(*) from extract_df) "portfolio %",
    count(case when offer!='' then flyer_item else null end)*1.00 / count(flyer_item) "offer items %",
    count(case when discount is not null then flyer_item else null end) / count(flyer_item) "discount items %",
    sum(discount) / sum(case when discount is not null then regular_price else null end) "avg. discount %",
    sum(instalment_mth) / sum(case when instalment_mth is not null then offer_price else null end) "avg. instl./mth %"
from extract_df
where flyer_cat is not null
group by 1
'''
anlys_df = duckdb.query(qry).df()


# In[15]:


## ETL transform - share
qry = '''
pivot
    (select flyer_cat "flyer - category", concat(platform, ' items') platform, count(flyer_item) items
    from extract_df
    where flyer_cat is not null
    group by 1, 2
    ) tbl1
on platform
using sum(items)
'''
share_df = duckdb.query(qry).df()


# In[16]:


## ETL transform - discount
qry = '''
pivot
    (select flyer_cat "flyer - category", concat(platform, ' discount %') platform, sum(discount) / sum(case when discount is not null then regular_price else null end) "avg. discount %",
    from extract_df
    where flyer_cat is not null
    group by 1, 2
    ) tbl1
on platform
using sum("avg. discount %")
'''
discount_df = duckdb.query(qry).df()


# In[17]:


## ETL load
clear = sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Furniture - Flyers").execute()
reqst = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="'Furniture - Flyers'!A1", valueInputOption="USER_ENTERED", body={"values": [flyer_df.columns.values.tolist()] + flyer_df.fillna("").values.tolist()}).execute()
reqst = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="'Furniture - Flyers'!M1", valueInputOption="USER_ENTERED", body={"values": [sumry_df.columns.values.tolist()] + sumry_df.fillna("").values.tolist()}).execute()
reqst = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="'Furniture - Flyers'!W1", valueInputOption="USER_ENTERED", body={"values": [anlys_df.columns.values.tolist()] + anlys_df.fillna("").values.tolist()}).execute()
reqst = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="'Furniture - Flyers'!AH1", valueInputOption="USER_ENTERED", body={"values": [share_df.columns.values.tolist()] + share_df.fillna("").values.tolist()}).execute()
reqst = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="'Furniture - Flyers'!AN1", valueInputOption="USER_ENTERED", body={"values": [discount_df.columns.values.tolist()] + discount_df.fillna("").values.tolist()}).execute()


# In[18]:


# ## sanity 
# qry = '''
# select flyer_item
# from extract_df
# where 
#     platform='Walmart'
#     and flyer_cat='Table+Chair+Desk'
# '''
# lst = duckdb.query(qry).df()['flyer_item'].tolist()
# for l in lst: print(l)


# In[19]:


## end
driver.close()
print("Listings in result: " + str(flyer_df.shape[0]))
print("Elapsed time to report (sec): " + str(round(time.time() - start_time)))


# In[ ]:




