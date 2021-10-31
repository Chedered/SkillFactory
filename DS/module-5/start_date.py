import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from multiprocessing import Pool
from itertools import zip_longest


test_data = pd.read_csv('test.csv')
test_data['price'] = 0
data = pd.read_csv('autoru-all-data.csv')
data = test_data.append(data, sort=False).reset_index(drop=True)

def chunks(lst, count):
    n = len(lst) // count
    return list(x for x in zip_longest(*[iter(lst)] * n))

all_url_lst = chunks(data['car_url'], len(data['car_url'])//1000)
temp_tpl = tuple(filter(None, all_url_lst[-1]))
all_url_lst.pop(-1)
all_url_lst.append(temp_tpl)

def get_start_date(url):
    response = ''
    while response == '':
        try:
            response = requests.get(url)
            break
        except:
            time.sleep(5)
            continue

    if response.status_code != 200:
        return None

    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        start_date = soup.find('div', class_='CardHead__infoItem CardHead__creationDate').text
    except:
        return None
    return start_date

if __name__ == '__main__':
    results = []
    for url_lst in tqdm(all_url_lst):
        with Pool() as p:
            results += p.map(get_start_date, tqdm(url_lst))
    # print(results)
    # temp_df = pd.DataFrame(results)
    # temp_df.to_csv('temp.csv', index=False)
    data['start_data'] = results
    data['start_data'].to_csv('start_date.csv', index=False)
