from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

def send_messages(inputs, is_running_fn):
    username = inputs['username']
    password = inputs['password']
    targets = inputs['targets']
    messages = inputs['messages']

    driver = webdriver.Chrome()
    driver.get('https://www.instagram.com/')
    time.sleep(3)

    # 🔐 Login
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password + Keys.RETURN)
    time.sleep(5)

    # ❌ Close popups
    for _ in range(2):
        try:
            driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()
            time.sleep(2)
        except:
            pass

    # 🔁 Loop
    while is_running_fn():
        for user in targets:
            if not is_running_fn():
                break

            driver.get(f'https://www.instagram.com/{user}/')
            time.sleep(3)
            try:
                driver.find_element(By.XPATH, "//button[contains(text(), 'Message')]").click()
                time.sleep(2)
                textarea = driver.find_element(By.TAG_NAME, 'textarea')

                for msg in messages:
                    textarea.send_keys(msg)
                    textarea.send_keys(Keys.SHIFT + Keys.RETURN)
                    time.sleep(1)

                textarea.send_keys(Keys.RETURN)
                print(f"✅ Sent to {user} at {datetime.now().strftime('%I:%M:%S %p')}")
                time.sleep(5)
            except Exception as e:
                print(f"⚠️ Failed for {user}: {e}")
                time.sleep(3)

        print("🔄 Cycle complete. Waiting before next round...")
        time.sleep(600)

    print("🛑 Messaging stopped.")
    driver.quit()
