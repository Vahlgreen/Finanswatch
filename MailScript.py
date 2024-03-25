import smtplib
from email.mime.text import MIMEText
import itertools
import random
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from faker import Faker
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def SendEmail(subject, body, sender, recipients, pw):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["Body"] = body
    msg["sender"] = sender
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        print("Connecting to server..")
        smtp_server.login(sender, pw)
        print("Connected successfully")
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Email send")


def StartTrial(mail, pw):
    # create account url
    url = "https://finanswatch.dk/profile/create?redirectUrl=https%3A%2F%2Flogin.watchmedier.dk%2Fauth%2Frealms%2Fwatchmedier%2Fprotocol%2Fopenid-connect%2Fauth%3Fsite%3Dfinanswatch.dk%26ui_locales%3Dda%26scope%3Dopenid%2Bprofile%2Bemail%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Ffinanswatch.dk%252Fauth%252Fcallback%253Fclient_name%253DKeycloakOidcClient_finanswatch.dk%26state%3Dc679a4b46c%26code_challenge_method%3DS256%26client_id%3Dwatch%26code_challenge%3DzVSfzKCs98mpivvxmfNqw8A7FrrdTo2wIEbITt0zmag"

    # initiate browser

    # Edge, virker lokalt, men ikke på pe server
    # options = webdriver.EdgeOptions()
    # options.add_argument("--headless=new")
    # driver = webdriver.Edge(options=options)
    # driver.implicitly_wait(2) #Time.sleep virker bedre

    # chrome, lokalt
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)

    # open browser
    driver.get(url)

    time.sleep(1)
    # cookies
    try:
        driver.find_element(By.XPATH, "//*[@id='CybotCookiebotDialogBodyButtonDecline']").click()
    except:
        print("No cookies found")
    fake = Faker()
    fakeName = fake.name().split(" ")

    print(fakeName)

    # username
    driver.find_element(By.XPATH, '// *[ @ id = ":R59clnlttbq5la:"]').send_keys(mail)
    time.sleep(1)
    # password
    driver.find_element(By.XPATH, '//*[@id=":R1aclnlttbq5la:"]').send_keys(pw)
    time.sleep(1)
    # firstname
    driver.find_element(By.XPATH, '//*[@id=":R1bclnlttbq5la:"]').send_keys(fakeName[0])
    time.sleep(1)
    # lastname
    driver.find_element(By.XPATH, '//*[@id=":R1cclnlttbq5la:"]').send_keys(" ".join(fakeName[1:]))
    time.sleep(1)
    # accept terms
    driver.find_element(By.XPATH, '//*[@id="createUserAcceptTerms"]').click()
    time.sleep(1)
    # create account
    driver.find_element(By.XPATH, '/html/body/div[3]/div/main/div/div/div/div/form/button').click()
    time.sleep(1)
    # login page
    driver.get("https://finanswatch.dk/auth/login?redirectTo=https%3A%2F%2Ffinanswatch.dk%2F")

    try:
        driver.find_element(By.XPATH, "//*[@id='CybotCookiebotDialogBodyButtonDecline']").click()
    except:
        print("No cookies found")

    driver.find_element(By.XPATH, '// *[ @ id = "username"]').send_keys(mail)
    time.sleep(1)
    driver.find_element(By.XPATH, '// *[ @ id = "password"]').send_keys(pw)
    time.sleep(1)
    driver.find_element(By.XPATH, '// *[ @ id = "password"]').send_keys(Keys.ENTER)

    # paywalled article
    driver.get("https://finanswatch.dk/Finansnyt/Pengeinstitutter/article16930818.ece")

    try:
        driver.find_element(By.XPATH, "//*[@id='CybotCookiebotDialogBodyButtonDecline']").click()
    except:
        print("No cookies found")
    time.sleep(1)
    # start trial
    driver.find_element(By.XPATH,
                        '//*[@id="__next"]/div/div/div[2]/div[1]/div/main/div/div/article[1]/div[5]/div/div/article/ul/li[1]/button').click()

    driver.quit()


def main():
    # test symbols
    # symbols = ["a","b", "c", "d", "e", "f", ".", "g", "h", "i", "j", "k", "l", "m", "n",
    #           "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y"]
    # prod symbols
    symbols = ["b", "c", "d", "e", "f", ".", "g", "h", "i", "j", "k", "l", "m", "n",
               "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "-", "!", "?"]
    numbers = [str(num) for num in range(1, 11)]


    emailCombos = list(itertools.combinations(symbols, 20))
    fwEmail = "".join(random.sample(emailCombos, 1)[0]) + '@gmail.com'
    pwCombos = list(itertools.combinations(numbers, 8))
    fwPassword = "".join(random.sample(pwCombos, 1)[0])

    StartTrial(fwEmail, fwPassword)

    subject = "Nyt login til Finanswatch!"
    body = f"Dit nye login kommer her \n brugernavn: {fwEmail}\n adgangskode: {fwPassword} \n\n\n Github repo: https://github.com/Vahlgreen/Finanswatch"

    with open("credentials.txt") as f:
        lines = f.readlines()
        sender = lines[0].strip()
        recipients = list(lines[1].strip().split(","))
        pw = lines[2].strip()

    SendEmail(subject, body, sender, recipients, pw)


main()
