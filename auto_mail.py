import os
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd


def login(user, pwd):
    user_box = browser.find_element_by_id('rcmloginuser')
    user_box.send_keys(user)  # admn no here
    secret_box = browser.find_element_by_id('rcmloginpwd')
    secret_box.send_keys(pwd)  # password here
    login_btn = browser.find_element_by_id('rcmloginsubmit')
    login_btn.click()


db = pd.read_csv('mail.csv', sep=',', encoding='1253', dtype=str)

chrome_options = Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome('./chromedriver.exe', options=chrome_options)
browser.get(os.environ['URL'])
time.sleep(1)
login(os.environ['USER'], os.environ['PWD'])
base = os.path.join('src', 'debts')


def send_msg(receiver, subject, text):
    def switch_body():
        ''' A function to switch back to the top of the message '''
        body = browser.find_element_by_xpath('//*[@id="composebody"]')
        time.sleep(2)
        body.click()
        ActionChains(browser) \
            .key_down(Keys.CONTROL) \
            .key_down(Keys.HOME) \
            .perform()

    def pick_font():
        ActionChains(browser) \
            .key_down(Keys.CONTROL) \
            .key_down(Keys.SHIFT) \
            .key_down(Keys.HOME) \
            .key_up(Keys.CONTROL) \
            .key_up(Keys.SHIFT) \
            .key_up(Keys.HOME) \
            .perform()

        time.sleep(0.1)
        browser.find_element_by_xpath('//*[@id="mceu_16-open"]').click()  # open font menu
        time.sleep(0.1)
        browser.find_element_by_xpath('//*[@id="mceu_45"]').click()  # pick font
        time.sleep(0.1)
        browser.find_element_by_xpath('//*[@id="mceu_17-open"]').click()  # open font size menu
        time.sleep(0.1)
        browser.find_element_by_xpath('//*[@id="mceu_65"]').click()  # pick size

    browser.find_element_by_xpath('//*[@id="rcmbtn108"]').click()  # create a new message
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(3)

    browser.find_element_by_xpath('//*[@id="_to"]').send_keys(receiver)  # enter the receiver
    time.sleep(0.2)
    browser.find_element_by_xpath('//*[@id="compose-subject"]').send_keys(subject)  # enter subject
    time.sleep(0.2)
    switch_body()
    time.sleep(0.2)
    for i in text:
        browser.find_element_by_xpath('//*[@id="composebody"]').send_keys(i)
        browser.find_element_by_xpath('//*[@id="composebody"]').send_keys(Keys.ENTER)
    time.sleep(0.2)
    browser.find_element_by_xpath('//*[@id="composeoptions"]/span[1]/label/select').click()  # open option menu
    time.sleep(0.2)
    browser.find_element_by_xpath('//*[@id="composeoptions"]/span[1]/label/select/option[1]').click()  # pick html
    alert = browser.switch_to.alert  # switch to alert
    alert.accept()  # accept the alert

    time.sleep(5)
    pick_font()
    browser.find_element_by_xpath('//*[@id="rcmbtn107"]').click()  # send message
    time.sleep(5)


def send_mail(path, name):
    time.sleep(1)
    recon = db[db['AFM'] == name]
    if not recon.empty:
        if len(recon) == 1:
            send = recon[recon.columns[5]].values[0]
            with open(path, encoding='1253') as f:
                reader = f.readlines()
                send_msg('pantelis@epilogic.gr', 'Debt\'s and Adjustment\'s', reader)
                time.sleep(1)
                print(f'[+] {name} Mail sent to: {send} ')

        else:
            raise Exception(ValueError)


if __name__ == '__main__':

    for i in os.listdir(base):
        try:
            send_mail(os.path.join('cook', i, i + '.txt'), i)
        except Exception as err:
            print(f'[!] Καμία οφειλή για : {i}')
