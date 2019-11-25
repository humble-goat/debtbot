import os
import time
import itertools
from io import BytesIO

import pandas as pd
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def take_screenshot(position, person, num, soup, tag, type, name):
    browser.implicitly_wait(50)
    time.sleep(1)
    table = soup.findAll(tag, {type: name})[0]
    time.sleep(1)
    xmap = xpath_soup(table)
    element = browser.find_element_by_xpath(xmap)
    location = element.location
    size = element.size
    png = browser.get_screenshot_as_png()
    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    im = im.crop((left, top, right, bottom))  # defines crop points
    if 'DEBTS' in ' '.join(position.split('/')[3:]).rstrip(' '):
        type_of_debt = 'DEBT'
    else:
        type_of_debt = 'ADJUSTMENT'
    im.save(f'{position}{person + f" {type_of_debt} " + str(num + 1)}.png')


def login(user, pwd):
    browser.implicitly_wait(50)

    usr = browser.find_element_by_id('username')
    usr.send_keys(user)  # admn no here
    passwd = browser.find_element_by_id('password')
    passwd.send_keys(pwd)  # password here
    time.sleep(1)
    browser.find_element_by_class_name('navbtn').click()
    time.sleep(1)
    # καρτέλα οφειλών
    time.sleep(1)
    browser.get('https://www1.gsis.gr/taxisnet/info/protected/displayDebtInfo.htm')
    # Στοιχεία ρύθμισης


def make_single_debt():
    browser.implicitly_wait(50)
    id_soup = BeautifulSoup(browser.page_source, features="html.parser")
    browser.implicitly_wait(50)
    single_debts = id_soup.findAll("div", {"class": "navbtn"})
    browser.implicitly_wait(50)
    # if id_soup.find_all('td', {'class': 'wintxt'})[-1].text == 'Δεν βρέθηκαν εγγραφές':
    #     log_off()
    # else:
    try:
        for point, i in enumerate(single_debts):
            time.sleep(1)
            target = xpath_soup(single_debts[point])
            browser.find_element_by_xpath(target).click()
            browser.implicitly_wait(50)
            time.sleep(1)
            debt_soup = BeautifulSoup(browser.page_source, features="html.parser")
            person_is = ' '.join(debt_soup.findAll('fieldset')[0].text.replace('\n', ' ').rstrip(' ').split(' ')[6:7])
            person_is = person_is.replace('\t', "")
            positiony = f"./src/ofeiles/{person_is}/DEBTS/"
            if not os.path.exists(positiony):
                os.makedirs(positiony)
            with open(f'{positiony}{person_is + " " + str(point + 1)}.txt', 'w+') as f:
                f.write(debt_soup.findAll('fieldset')[1].text)
            take_screenshot(positiony, person_is, point, debt_soup, 'td', 'class', 'pageBgIn')
            browser.back()
            browser.implicitly_wait(50)
            time.sleep(1)

    except Exception as error:
        print(f'Something is wrong with this person:: {name} {pwd} {point}', error)


def make_rhyme():
    time.sleep(1)
    browser.implicitly_wait(50)
    browser.get('https://www1.gsis.gr/taxisnet/info/protected/displayArrangementInfo.htm')
    rythmisi_soup = BeautifulSoup(browser.page_source, features='html.parser')

    try:
        rhyme = rythmisi_soup.findAll("div", {"class": "navbtn"})
        for count, i in enumerate(rhyme):
            time.sleep(1)
            target = xpath_soup(rhyme[count])
            browser.find_element_by_xpath(target).click()
            try:
                WebDriverWait(browser, 2).until(EC.alert_is_present(),
                                                'Timed out waiting for PA creation ' +
                                                'confirmation popup to appear.')

                alert = browser.switch_to.alert
                alert.accept()
                print("Alert accepted")
            except TimeoutException:
                pass
            rhyme_soup = BeautifulSoup(browser.page_source, features="html.parser")
            person_is = ' '.join(rhyme_soup.findAll('fieldset')[0].text.replace('\n', ' ').rstrip(' ').split(' ')[6:7])
            person_is = person_is.replace('\t', '')
            positiony = f'./src/ofeiles/{person_is}/ADJUSTMENT/'
            if not os.path.exists(positiony):
                os.makedirs(positiony)
            with open(f'{positiony}{person_is + " " + str(count + 1)}.txt', 'w+') as f:
                f.write(rhyme_soup.findAll('fieldset')[1].text)
            take_screenshot(positiony, person_is, count, rhyme_soup, 'td', 'class', 'pageBgIn')
            browser.back()
            browser.implicitly_wait(50)
            time.sleep(1)
            # log_off()

    except Exception as err:
        print(f'Something is wrong with this person at adjustments:: {name} {pwd} {count}', err)


if __name__ == '__main__':

    dirname = os.path.abspath(__file__)
    url = 'https://www1.gsis.gr/taxisnet/mytaxisnet'

    start = time.perf_counter()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    cromium_path = os.path.split(dirname)[0] + '\\chromedriver.exe'
    db = pd.read_csv(os.environ['DB'], sep=',', encoding='1253', dtype=str)
    for name, pwd in zip(db[db.columns[3]].values, db[db.columns[4]].values):
        print(f'[+] {db.loc[db[db.columns[3]] == name, db.columns[0]].values[0]} {db.loc[db[db.columns[3]] == name, db.columns[1]].values[0]}')
        browser = webdriver.Chrome(cromium_path, options=chrome_options)
        browser.implicitly_wait(30)
        browser.get(url)
        time.sleep(2)
        login(name, pwd)
        time.sleep(1)
        browser.implicitly_wait(50)
        make_single_debt()
        browser.implicitly_wait(50)
        time.sleep(1)
        make_rhyme()
        browser.quit()

    end = time.perf_counter()
    print(f'Elapsed time:{end-start}')
    browser.quit()
