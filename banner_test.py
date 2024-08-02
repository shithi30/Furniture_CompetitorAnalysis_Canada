# import
from pyvirtualdisplay import Display
import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# setup
Display(visible = 0, size = (1920, 1080)).start() 
options = webdriver.ChromeOptions().add_argument("ignore-certificate-errors")

# window
driver = webdriver.Chrome(options = options)
driver.maximize_window()

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
    
# end
driver.close()

