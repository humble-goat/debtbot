import os
import re
import time

import pandas as pd

db = pd.read_csv(os.environ['DB'], encoding='1253', sep=',', dtype=str)


def made_debts(path, name):
    my_path = os.path.abspath('./mixed_data/' + name)
    no_date = os.path.abspath('./mixed_data/no_date/debt/')
    for count, i in enumerate(os.listdir(path)):
        if i.split('.')[-1] == 'txt':
            with open(os.path.join(path, i)) as f:
                reader = f.readlines()
                dosage = reader[25]
                total_debt = reader[21]
                reason = reader[13]
                id = reader[29]
                if re.findall('([1-9]{1,2}[.\/-]{1}([1-9]|1[012])[.\/-]{1}[0-9]{2,4})', reader[-12].replace('\n', '')):
                    date = \
                    re.findall('([1-9]{1,2}[.\/-]{1}([1-9]|1[012])[.\/-]{1}[0-9]{2,4})', reader[-12].replace('\n', ''))[
                        0][0]

                    if not os.path.isdir(my_path):
                        os.mkdir(my_path)
                    if count == 0:
                        with open(os.path.join(my_path, name + '.txt'), mode='w+') as file:
                            file.write('Debt for person: ' + true_name + '\n')
                            file.write('Reason: ' + reason + '\n')
                            file.write('Σύνολο οφειλής: ' + total_debt + '\n')
                            file.write('Dosage Deadline: ' + date + '\n')
                            file.write('Dosage price: ' + dosage + '\n')
                            file.write('Debt ID: ' + id)
                    else:
                        with open(os.path.join(my_path, name + '.txt'), mode='a+') as file:
                            file.write('\n')
                            file.write('Debt for person: ' + true_name + '\n')
                            file.write('Reason: ' + reason + '\n')
                            file.write('Σύνολο οφειλής: ' + total_debt + '\n')
                            file.write('Dosage Deadline: ' + date + '\n')
                            file.write('Dosage price: ' + dosage + '\n')
                            file.write('Debt ID: ' + id)
                else:
                    with open(os.path.join(no_date, name + '.txt'), mode='w+') as file:
                        file.write(name + '\n')
                        file.write(reason + '\n')
                        file.write(dosage + '\n')
        elif i.split('.')[-1] == 'png':
            pass


def make_rhyme(path, name):
    my_path = os.path.abspath('./mixed_data/' + name)
    no_date = os.path.abspath('./mixed_data/no_date/adjustments/')
    for count, i in enumerate(os.listdir(path)):
        if i.split('.')[-1] == 'txt':
            with open(os.path.join(path, i)) as f:
                reader = f.readlines()
                dosage = reader[17]
                reason = reader[9]
                id = reader[21]
                if re.findall('([1-9]{1,2}[.\/-]{1}([1-9]|1[012])[.\/-]{1}[0-9]{2,4})', reader[16].replace('\n', '')):
                    date = \
                        re.findall('([1-9]{1,2}[.\/-]{1}([1-9]|1[012])[.\/-]{1}[0-9]{2,4})',
                                   reader[16].replace('\n', ''))[
                            0][0]

                    if not os.path.isdir(my_path):
                        os.mkdir(my_path)
                        with open(os.path.join(my_path, name + '.txt'), mode='w+') as file:
                            file.write('\n')
                            file.write('Adjustment for person: ' + true_name + '\n')
                            file.write('Reason: ' + reason + '\n')
                            file.write('Dosage Deadline: ' + date + '\n')
                            file.write('Dosage price: ' + dosage + '\n')
                            file.write('Adjustment ID: ' + id)
                    else:
                        with open(os.path.join(my_path, name + '.txt'), mode='a+') as file:
                            file.write('\n')
                            file.write('Adjustment for person: ' + true_name + '\n')
                            file.write('Reason: ' + reason + '\n')
                            file.write('Dosage Deadline: ' + date + '\n')
                            file.write('Dosage price: ' + dosage + '\n')
                            file.write('Adjustment ID: ' + id)
                else:
                    with open(os.path.join(no_date, name + '.txt'), mode='w+') as file:
                        file.write(name + '\n')
                        file.write(reason + '\n')
                        file.write(dosage + '\n')
        elif i.split('.')[-1] == 'png':
            pass


base = os.path.join('src', 'ofeiles')

for i in os.listdir(base):
    try:
        true_name = ' '.join([db.loc[db['VATID'] == i, 'LAST'].values[0], db.loc[db['VATID'] == i, 'NAME'].values[0]])
    except Exception as err:
        true_name = db.loc[db['VATID'] == i, 'LAST'].values[0]

    child_ofeiles = os.path.join(base, i, 'DEBTS')
    child_rhyme = os.path.join(base, i, 'ADJUSTMENT')
    if os.path.isdir(child_ofeiles):
        made_debts(child_ofeiles, i)
    if os.path.isdir(child_rhyme):
        make_rhyme(child_rhyme, i)
