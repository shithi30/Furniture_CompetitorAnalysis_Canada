#!/usr/bin/env python
# coding: utf-8

# In[1]:


## import
from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

chromedriver_autoinstaller.install() 


# In[2]:


## scrape

# pref.
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
options = webdriver.ChromeOptions().add_argument("ignore-certificate-errors")

# window
driver = webdriver.Chrome(options = options)
driver.maximize_window()


# In[3]:


## Canadian Tire

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


# In[4]:


## email

# summary

# from, to, body
sender_email = "shithi30@gmail.com"
recver_email = ["shithi30@outlook.com"]
body = str(img_links)

# object
html_msg = MIMEText(body, "html")
html_msg['Subject'] = "banner_trial"
html_msg['From'] = "Shithi Maitra"
html_msg['To'] = ", ".join(recver_email)

# send
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
   server.login(sender_email, "uhfu cppa sxgh bwpr")
   server.sendmail(sender_email, recver_email, html_msg.as_string())


# In[5]:


## end
driver.close()


# In[ ]:



