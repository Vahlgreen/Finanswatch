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
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import datetime
import os


def SendEmail(subject, body, error = False):
    # Find directory (explicitly, to avoid issues on pe server)
    script_directory = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_directory, "credentials.txt")

    # open credentials
    with open(data_file) as f:
        lines = f.readlines()
        sender = lines[0].strip()
        if error == False:
            recipients = list(lines[1].strip().split(","))
        else:
            recipients = list(lines[2].strip().split(","))
        pw = lines[3].strip()



    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["Body"] = body
    msg["sender"] = sender
    msg["To"] = ", ".join(recipients)

    # establish connection to smtp and send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        print("Connecting to server..")
        smtp_server.login(sender, pw)
        print("Connected successfully")
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Email send")


def StartTrial(mail, pw):
    # Edge, works locally
    # options = webdriver.EdgeOptions()
    # options.add_argument("--headless=new")
    # driver = webdriver.Edge(options=options)
    # driver.implicitly_wait(2) #Time.sleep virker bedre

    # chrome, works locally
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # chrome, works on PE server
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    # create account url
    url = "https://finanswatch.dk/profile/create?redirectUrl=https%3A%2F%2Flogin.watchmedier.dk%2Fauth%2Frealms%2Fwatchmedier%2Fprotocol%2Fopenid-connect%2Fauth%3Fsite%3Dfinanswatch.dk%26ui_locales%3Dda%26scope%3Dopenid%2Bprofile%2Bemail%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Ffinanswatch.dk%252Fauth%252Fcallback%253Fclient_name%253DKeycloakOidcClient_finanswatch.dk%26state%3Dc679a4b46c%26code_challenge_method%3DS256%26client_id%3Dwatch%26code_challenge%3DzVSfzKCs98mpivvxmfNqw8A7FrrdTo2wIEbITt0zmag"

    # open browser
    driver.get(url)

    # implicitly wait function seems to crash. Use sleep instead
    time.sleep(1)

    # check for cookies
    try:
        driver.find_element(By.XPATH, "//*[@id='CybotCookiebotDialogBodyButtonDecline']").click()
    except:
        print("No cookies found. Script continues..")

    # Faker object for name generation
    fake = Faker()
    fakeName = fake.name().split(" ")

    # interacting with registration formula
    # username
    driver.find_element(By.XPATH, '/html/body/div[3]/div/main/div/div/div/div/form/div[1]/div/input').send_keys(mail)
    time.sleep(1)
    # password
    driver.find_element(By.XPATH, '//*[@id=":R59imfjtt7qmja:"]').send_keys(pw)
    time.sleep(1)
    # firstname
    driver.find_element(By.XPATH, '/html/body/div[3]/div/main/div/div/div/div/form/div[3]/input').send_keys(fakeName[0])
    time.sleep(1)
    # lastname
    driver.find_element(By.XPATH, '//*[@id=":R5himfjtt7qmja:"]').send_keys(" ".join(fakeName[1:]))
    time.sleep(1)
    # accept terms
    driver.find_element(By.XPATH, '//*[@id="createUserAcceptTerms"]').click()
    time.sleep(1)
    # create account
    driver.find_element(By.XPATH, '/html/body/div[3]/div/main/div/div/div/div/form/button').click()
    time.sleep(1)

    # Navigate to login page
    driver.get("https://finanswatch.dk/auth/login?redirectTo=https%3A%2F%2Ffinanswatch.dk%2F")

    try:
        driver.find_element(By.XPATH, "//*[@id='CybotCookiebotDialogBodyButtonDecline']").click()
    except:
        print("No cookies found. Script continues..")

    # perform login
    driver.find_element(By.XPATH, '// *[ @ id = "username"]').send_keys(mail)
    time.sleep(1)
    driver.find_element(By.XPATH, '// *[ @ id = "password"]').send_keys(pw)
    time.sleep(1)
    driver.find_element(By.XPATH, '// *[ @ id = "password"]').send_keys(Keys.ENTER)

    # url for paywalled article
    driver.get("https://finanswatch.dk/Finansnyt/Pengeinstitutter/article16930818.ece")

    try:
        driver.find_element(By.XPATH, "//*[@id='CybotCookiebotDialogBodyButtonDecline']").click()
    except:
        print("No cookies found. Script continues..")

    time.sleep(5)
    # start trial
    try:
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div[1]/div/main/div/div/article[1]/div[5]/div/div/article/div/ul/li[1]/button").click()
    except Exception as e:
        pass
    time.sleep(10)
    driver.quit()

def create_password() -> str:
    validSymbols = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    random.shuffle(validSymbols)
    return "".join(validSymbols)

def create_email() -> str:
    validSymbols = 'abcdefghijklmnopqrstuvwxyz1234567890'
    length = random.randint(8, 15)
    login = ''
    for i in range(length):
        pos = random.randint(0, len(validSymbols) - 1)
        login = login + validSymbols[pos]

    # Don't start with numeric
    if login[0].isnumeric():
        pos = random.randint(0, len(validSymbols) - 10)
        login = validSymbols[pos] + login

    return login + '@gmail.com'

def main():

    # Generate email
    fwEmail = create_email()

    # Generate password
    fwPassword = create_password()


    # Start Trial and send the credentials. Retry once on error
    try:
        StartTrial(fwEmail, fwPassword)
        subject = "Nyt login til Finanswatch!"
        body = f"Dit nye login kommer her \n brugernavn: {fwEmail}\n adgangskode: {fwPassword} \n\n\n Github repo: https://github.com/Vahlgreen/Finanswatch"
        SendEmail(subject, body)
    except Exception as e:
        try:
            StartTrial(fwEmail, fwPassword)
            subject = "Nyt login til Finanswatch!"
            body = f"Dit nye login kommer her \n brugernavn: {fwEmail}\n adgangskode: {fwPassword} \n\n\n Github repo: https://github.com/Vahlgreen/Finanswatch"
            SendEmail(subject, body)
        except Exception as e:
            subject = "Fejl rapport: Finanswatch script"
            body = f"Efter to forsøg lykkedes det ikke at oprette en prøveperiode. Fejl: {e}"
            SendEmail(subject, body, error=True)


# today = datetime.date.today()
# weekday = today.weekday()
# if weekday == 0:
main()
