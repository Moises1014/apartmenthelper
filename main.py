import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

SERVER = smtplib.SMTP('smtp.gmail.com', 587)
EMAIL_USER = ''
EMAIL_SENT = ''
EMAIL_PSW = ''
SUBJECT = 'Apartments in Downtown Orlando'


def apartment_bot():
    # Use a breakpoint in the code line below to debug your script.
    apartment_li = []
    pageurl = 'https://www.apartments.com/apartments/downtown-orlando-orlando-fl/under-1300/1/'
    driver.get(pageurl)
    for i in range(1, 20):
        pagenum = str(i)
        name = driver.find_element_by_xpath(
            '//*[@id="placardContainer"]/ul/li[' + pagenum + ']/article/header/div[1]/a/div[1]/span').text
        address = driver.find_element_by_xpath(
            '//*[@id="placardContainer"]/ul/li[' + pagenum + ']/article/header/div[1]/a/div[2]').text
        rent = driver.find_element_by_xpath(
            '//*[@id="placardContainer"]/ul/li[' + pagenum + ']/article/section/div/div[2]/div/div[2]/div').text
        beds = driver.find_element_by_xpath(
            '//*[@id="placardContainer"]/ul/li[' + pagenum + ']/article/section/div/div[2]/div/div[3]/div[1]').text
        availability = driver.find_element_by_xpath(
            '//*[@id="placardContainer"]/ul/li[' + pagenum + ']/article/section/div/div[2]/div/div[3]/div[2]').text
        link = driver.find_element_by_xpath(
            '//*[@id="placardContainer"]/ul/li[' + pagenum + ']/article/header/div[1]/a').get_attribute('href')
        apartments = {
            'Name': name,
            'Location': address,
            'Rent': rent,
            'Rooms': beds,
            'Availability': availability,
            'Link': link,
        }
        apartment_li.append(apartments)
    driver.close()
    ans = pd.DataFrame(apartment_li)
    df_html = ans.to_html()
    dfpart = MIMEText(df_html, 'html')
    SERVER.starttls()
    SERVER.login(EMAIL_USER, EMAIL_PSW)

    msg = MIMEMultipart('alternative')

    msg['Subject'] = SUBJECT
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_SENT
    msg.attach(dfpart)
    SERVER.sendmail(EMAIL_USER, EMAIL_SENT, msg.as_string())
    SERVER.quit()
    print('email sent')

apartment_bot()