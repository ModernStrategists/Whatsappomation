from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
import os

from selenium.webdriver.chrome.service import Service

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


print(style.BLUE)
print("**********************************************************")
print("**********************************************************")
print("*****                                               ******")
print("*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******")
print("*****      This tool was built by ModernStrategists  ******")
print("*****                                               ******")
print("**********************************************************")
print("**********************************************************")
print(style.RESET)

# Load the message from the file
with open("message.txt", "r", encoding="utf8") as f:
    message = f.read()

print(style.YELLOW + '\nThis is your message:')
print(style.GREEN + message)
print("\n" + style.RESET)
message = quote(message)

numbers = []
with open("numbers.txt", "r") as f:
    for line in f.read().splitlines():
        if line.strip() != "":
            numbers.append(line.strip())

total_number = len(numbers)
print(style.RED + f'We found {total_number} numbers in the file' + style.RESET)
delay = 30


media_file_path = r'C:\Users\sutha\Downloads\Phiri.mp4'  # Example media file path


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

print('Once your browser opens up, sign in to WhatsApp Web.')
driver.get('https://web.whatsapp.com')
input(style.MAGENTA + "AFTER logging into WhatsApp Web is complete and your chats are visible, press ENTER..." + style.RESET)

# Sending messages and media to each number
for idx, number in enumerate(numbers):
    number = number.strip()
    if number == "":
        continue

    print(style.YELLOW + f'{idx + 1}/{total_number} => Sending message to {number}.' + style.RESET)
    try:
        url = f'https://web.whatsapp.com/send?phone={number}&text={message}'
        driver.get(url)
        sent = False
        for i in range(3):  # Retry up to 3 times
            if not sent:
                try:
                    # Wait for the send button to be clickable
                    send_button = WebDriverWait(driver, delay).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send']"))
                    )

                    # Wait for the attachment button (Photos & Videos)
                    attach_button = WebDriverWait(driver, delay).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@title='Attach']"))
                    )

                    # Click on the attachment button to open the media options
                    attach_button.click()

                    # Wait for the file input element to be clickable
                    file_input = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"))
                    )
                
                    # Upload the media file
                    file_input.send_keys(media_file_path)

                    send_button = WebDriverWait(driver, delay).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Send']"))
                    )
                    # Click the send button
                    sleep(4)
                    send_button.click()
                    sleep(3)

            

                except Exception as e:
                    print(style.RED + f"\nFailed to send message to: {number}, retry ({i + 1}/3) due to {str(e)}" + style.RESET)
                    print("Make sure your phone and computer are connected to the internet.")
                    print("If there is an alert, please dismiss it." + style.RESET)
                else:
                    sent = True
                    sleep(3)  # Wait for the message to send
                    print(style.GREEN + f'Message and media sent to: {number}' + style.RESET)
    except Exception as e:
        print(style.RED + f'Failed to send message to {number} due to {str(e)}' + style.RESET)

# Quit the browser after sending all messages
import pdb; pdb.set_trace()
driver.quit()
