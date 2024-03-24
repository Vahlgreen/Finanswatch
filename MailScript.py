import smtplib
from email.mime.text import MIMEText
import itertools
import random
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def SendEmail(subject,body,sender,recipients,pw):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["Body"] = body
    msg["sender"] = sender
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp_server:
        print("Connecting to server..")
        smtp_server.login(sender,pw)
        print("Connected successfully")
        smtp_server.sendmail(sender,recipients,msg.as_string())
        print("Email send")

def StartTrial(mail,pw):
    url = "https://finanswatch.dk/profile/create?redirectUrl=https%3A%2F%2Flogin.watchmedier.dk%2Fauth%2Frealms%2Fwatchmedier%2Fprotocol%2Fopenid-connect%2Fauth%3Fsite%3Dfinanswatch.dk%26ui_locales%3Dda%26scope%3Dopenid%2Bprofile%2Bemail%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Ffinanswatch.dk%252Fauth%252Fcallback%253Fclient_name%253DKeycloakOidcClient_finanswatch.dk%26state%3Dc679a4b46c%26code_challenge_method%3DS256%26client_id%3Dwatch%26code_challenge%3DzVSfzKCs98mpivvxmfNqw8A7FrrdTo2wIEbITt0zmag"
    # initiate browser
    driver = webdriver.Edge()
    driver.get(url)
    time.sleep(1)

    try:
        driver.find_element(By.XPATH, "//*[@id='CybotCookiebotDialogBodyButtonDecline']").click()
    except:
        print("Ingen cookies.. Fortsætter")

    driver.find_element(By.XPATH,'// *[ @ id = ":R59clnlttbq5la:"]').send_keys(mail)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id=":R1aclnlttbq5la:"]').send_keys(pw)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id=":R1bclnlttbq5la:"]').send_keys("peter")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id=":R1cclnlttbq5la:"]').send_keys("khan")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="createUserAcceptTerms"]').click()#
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div[3]/div/main/div/div/div/div/form/button').click()


    driver.get("https://finanswatch.dk/auth/login?redirectTo=https%3A%2F%2Ffinanswatch.dk%2F")
    try:
        driver.find_element(By.XPATH, "//*[@id='CybotCookiebotDialogBodyButtonDecline']").click()
    except:
        print("Ingen cookies.. Fortsætter")

    driver.find_element(By.XPATH, '// *[ @ id = "username"]').send_keys(mail)
    time.sleep(1)
    driver.find_element(By.XPATH, '// *[ @ id = "password"]').send_keys(pw)

    #driver.find_element(By.XPATH, "// *[ @ id = 'kc-sign-up']").click()


    #//*[@id="createUserAcceptTerms"]
    #/html/body/div[3]/div/main/div/div/div/div/form/button
    #passwordElement = driver.find_element(By.XPATH,"//*[@id='password']")


    #usernameElement.send_keys(mail)
    #passwordElement.send_keys(pw)
    #passwordElement.send_keys(Keys.ENTER)


    #
    #time.sleep(1)
    #driver.find_element(By.XPATH, "//*[@id='__next']/div/div/header/div[1]/div/div/nav[2]/ul[2]/li[2]/a/span").click()

    print("test")
def main():

    letters = ["a", "b", "c", "d", "e", "f", ".", "g", "h", "i", "j", "k", "l", "m", "n",
               "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "-"]
    numbers=[str(num) for num in range(1,11)]

    emailCombos = list(itertools.combinations(letters, 20))
    fwEmail = "".join(random.sample(emailCombos, 1)[0]) + '@gmail.com'
    pwCombos = list(itertools.combinations(numbers, 10))
    fwPassword = "".join(random.sample(pwCombos, 1)[0])


    subject = "Nyt login til Finanswatch!"
    body = f"Dit nye login kommer her \nbrugernavn: {fwEmail}\npassword: {fwPassword}"
    sender = "frankfyr73@gmail.com"
    pw = "ylmp xblq zcqj bqke"#app password
    recipients = [sender, "vahlgreen@live.dk"]

    StartTrial(fwEmail,fwPassword)
    #SendEmail(subject,body,sender,recipients,pw)


main()
