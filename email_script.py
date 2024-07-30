## Databricks email

# import
import smtplib
from email.mime.text import MIMEText

# summary
# oos = ola_df_pres['skus_gone_oos'].tolist()[0]
oos = "\U000026D4 Out of Stock: <i>" # + oos[2:].replace("\n- ", ", ") + "</i><br>" if len(oos)>2 else ""
# ats = ola_df_pres['skus_added_to_stock'].tolist()[0]
ats = "\U00002705 Added to Stock: <i>" # + ats[2:].replace("\n- ", ", ") + "</i><br>" if len(ats)>2 else ""

# from, to, body
sender_email = "shithi30@gmail.com"
recver_email = ["maitra.shithi.aust.cse@gmail.com", "shithi30@outlook.com"]
body = oos + ats + "<br>"

# object
html_msg = MIMEText(body, "html")
html_msg['Subject'] = "Git Actions Email"
html_msg['From'] = "Shithi Maitra"
html_msg['To'] = ", ".join(recver_email)

# send
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
   server.login(sender_email, "uhfu cppa sxgh bwpr")
   if len(oos + ats) > 0: server.sendmail(sender_email, recver_email, html_msg.as_string())
