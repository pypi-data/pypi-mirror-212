import sys
import keyring
import api_secrets as api_secrets
import requests
import time
import json
from pathlib import Path
import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


  
def initiate_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

def get_token(system, grant_type, token_user, client_id, user, scope):
    def refresh_token():
        
        secret = api_secrets.get_secret(system, user)
        if not secret:
            print(f"No credentials found. Please ensure you have set system: {system} and user: {user} in write_secret.py keyring manager")
            x = input("Press enter to exit")
            sys.exit()

        url = secret["url"]
        client_secret = secret["secret"]
        oauth_url = secret["oauth_url"]
        redirect_uri = "http://localhost:8080"

        if grant_type == "authorization_code":
            code_url = f"{oauth_url}/authorizations/new?client_id={client_id}&response_type=code&scope={scope}&redirect_uri={redirect_uri}"
            try:
                print("initiating driver window")
                driver = initiate_driver()
                driver.get(code_url)
                wait = WebDriverWait(driver, 120)
                wait.until(EC.url_contains("http://localhost:8080"))
                browser_url = driver.current_url
                code = browser_url.split("?code=")[1]
                print("successfully received code")
                driver.quit()
            except IndexError:
                print("Got error fetching code from browser - maybe timeout? Please try again")
                x = input("Press enter to exit")
                driver.quit()
                sys.exit()

            token_url = f"{oauth_url}/token?client_id={client_id}&grant_type=authorization_code&code={code}&scope={scope}&client_secret={client_secret}&redirect_uri={redirect_uri}"

        elif grant_type == "client_credentials":
            token_url = f"{oauth_url}/token?client_id={client_id}&grant_type=client_credentials&scope={scope}&client_secret={client_secret}"
        
        else:
            print(f"Invalid grant_type specified {grant_type}")
            x = input("Press enter to exit")
            sys.exit()
        print(f'Making URL request for token to {token_url}')
        r = requests.post(token_url)
        if r.status_code == 200:
            print("Successfully received token")
            result = json.loads(r.content)
            current_time = time.time()
            result["epoch_expiry"] = current_time + result["expires_in"] #set the real drop dead time of token
            result["url"] = url
            return result
        else:
            print("Couldn't fetch token")
            print(r.content)
            print(r.status_code)
            x = input("Press enter to exit")
            sys.exit()

    secret_token = api_secrets.get_secret(system, token_user)
    current_time = time.time()

    if not secret_token: #no user stored token
        print("No token stored - fetching")
        secret_token = refresh_token()
        print(f"Setting token for system {system} and token {token_user} for secret_token (len = {len(json.dumps(secret_token))})")
        api_secrets.write_secret(system, token_user, secret_token)

    elif secret_token["epoch_expiry"] < current_time + 3600:
        print("Token expired - refreshing")
        secret_token = refresh_token()
        print(f"Setting token for system {system} and token {token_user} for secret_token (len = {len(json.dumps(secret_token))})")
        api_secrets.write_secret(system, token_user, secret_token)
        
    else:
        print("Have valid token - using to make API call(s)")

    return secret_token
