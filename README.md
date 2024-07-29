This repository enlists my complete works on Canada's competitive furniture eCommerce market analysis. <br>
→ Toolset/Tech Stack: ```Python``` ```Selenium webdriver``` ```regex``` ```GCP - GSheets API``` ```PIL``` ```duckdb``` ```win32com.client``` <br>
→ Latest data can be found [here](https://docs.google.com/spreadsheets/d/1rvnYmn4-6T37GqeUFbRieY2uGYu8qg8ng62YGDjoc8M/edit?usp=sharing).

### Similarweb Traffic - Competitive Analysis
<p align="center">
  <img width="935" alt="c5" src="https://github.com/user-attachments/assets/c1c62d87-71dd-4176-bbf6-6c4bc43e7ca0"><br>
  <img width="755" alt="ee8" src="https://github.com/user-attachments/assets/5236db31-f627-42bd-8879-9d6b85fc0580">
</p>

### Competitor Banners - Daily Reporting 
<p align="center">
<img width="900" alt="c4" src="https://github.com/user-attachments/assets/8338942a-752b-48cd-9e2b-a63938127444"><br>
<img width="680" alt="c4" src="https://github.com/user-attachments/assets/53d77a5f-d535-4086-bee4-ebed73e031e8">

### Competitor Banners - Caller Function
```Python
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
```  
</p>

### Daily Stocks - Prices & Fluctuations
<p align="center">
  <img width="750" alt="c5" src="https://github.com/user-attachments/assets/c7ff1510-7dc2-4e71-a2f7-f9de1e325702"><br>
</p>

### Flyer Analytics - Competitive Landscape
<p align="center">
  <img width="570" alt="c1" src="https://github.com/user-attachments/assets/82968186-ccf6-47ca-9b85-e770604d7090"><br>
  <img width="827" alt="c2" src="https://github.com/user-attachments/assets/4c173c6d-e139-4558-9f25-99bc5c28e7b4"><br>
  <img width="670" alt="c3" src="https://github.com/user-attachments/assets/6a7283a0-a4e5-4541-b2d8-53418d33936e"><br>
  <img width="700" alt="c3" src="https://github.com/user-attachments/assets/4a232415-9858-4142-8da5-bdc28dbcff5e">
</p>
