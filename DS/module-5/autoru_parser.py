import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from datetime import date
from multiprocessing import Pool

brands_list = ['SKODA',
               'AUDI',
               'HONDA',
               'VOLVO',
               'BMW',
               'NISSAN',
               'INFINITI',
               'MERCEDES',
               'TOYOTA',
               'LEXUS',
               'VOLKSWAGEN',
               'MITSUBISHI']


def get_max_page(brand):
    response = requests.get(f'https://auto.ru/moskva/cars/{brand}/used/')
    soup = BeautifulSoup(response.text, 'lxml')
    pages = soup.find(
        'span', class_='ControlGroup ControlGroup_responsive_no ControlGroup_size_s ListingPagination__pages')
    max_page = int(pages.find_all('span', class_='Button__text')[-1].text)
    return max_page


def get_param(brand, page):
    param = {
        "category": "cars",
        "section": "used",
        "catalog_filter": [{"mark": brand}],
        "page": page,
        "geo_radius": 200,
        "geo_id": [213]
    }
    return param


def get_headers(brand, page):
    headers = f'''
Host: auto.ru
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0
Accept: */*
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://auto.ru/moskva/cars/{brand}/used/?page={page}
x-client-app-version: fc2932d200d
x-page-request-id: 14721e109a8a263b47dcef08d7daa8c7
x-client-date: {int(round(time.time(), 3)*1000)}
x-csrf-token: b67177e46b40cc0938201d6add6543f6d8b01407c60dfe78
x-requested-with: fetch
content-type: application/json
Origin: https://auto.ru
Content-Length: 112
Connection: keep-alive
Cookie: suid=b82b1360a9cce2355897aadee2636626.f4d44d07389f12d728062e2cea4b2aec; _csrf_token=b67177e46b40cc0938201d6add6543f6d8b01407c60dfe78; autoru_sid=a%3Ag6176eb732coj9q16e3n8h9e5omgpacn.d795fd04efb17e2a3b86396dc5cac4b1%7C1635183475903.604800.LF2Hyxf7sEx06WNYkwr2Bg.Y_Z-QGmY2PjZPgvgCtCTWirX21_1yFvxDpsOzmN7rCg; autoruuid=g6176eb732coj9q16e3n8h9e5omgpacn.d795fd04efb17e2a3b86396dc5cac4b1; from_lifetime=1635184525442; from=direct; X-Vertis-DC=sas; yuidlt=1; yandexuid=7127153541604003384; my=YwA%3D; crookie=g/G4q1/cHpkS2ByfKgZMeN+LDW+2Z7tCBnQv7PLopkGEY0+o5C6Y1sjFSIb7KvxLpCESCvaR7EZ1OMcehpJf92hqGjY=; cmtchd=MTYzNTE4MzQ4Mjk1OA==; gdpr=0; _ym_uid=1635183483662690441; _ym_d=1635184525; cycada=sIK8EDyagkn5foGrW7t7sX5vJGobFwB8hMAlOzjQGY8=; _ym_isad=2
'''
    headers = {line.split(': ')[0]: line.split(': ')[1] for line in headers.strip().split('\n')}
    return headers


def get_json(param, headers):
    url = 'https://auto.ru/-/ajax/desktop/listing/'
    offers = ''
    while offers == '':
        try:
            response = requests.post(url, json=param, headers=headers)
            offers = response.json()['offers']
            break
        except:
            time.sleep(5)
            continue

    return offers


def get_car_dict(car):
    try:
        price = car['price_info']['RUR']
    except KeyError:
        return False

    brand = car['vehicle_info']['mark_info']['name']
    model = car['vehicle_info']['model_info']['name']
    sell_id = car['saleId']
    section = car['section']
    car_url = f'https://auto.ru/cars/{section}/sale/{brand.lower()}/{model.lower()}/{sell_id}/'

    response = ''
    while response == '':
        try:
            response = requests.get(car_url)
            break
        except:
            time.sleep(5)
            continue

    if response.status_code != 200:
        return False
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    card_info = soup.find('ul', class_='CardInfo')

    try:
        color = card_info.find('li', class_='CardInfoRow CardInfoRow_color')
        color = color.find('a').text
    except AttributeError:
        color = None

    try:
        fuelType = card_info.find(
            'li', class_='CardInfoRow CardInfoRow_engine')
        fuelType = fuelType.find('a').text
    except AttributeError:
        fuelType = None

    try:
        ownersCount = card_info.find(
            'li', class_='CardInfoRow CardInfoRow_ownersCount')
        ownersCount = ownersCount.find_all('span')[1].text
        ownersCount = ownersCount.replace('\xa0', ' ')
    except AttributeError:
        ownersCount = None

    try:
        owningTime = card_info.find(
            'li', class_='CardInfoRow CardInfoRow_owningTime')
        owningTime = owningTime.find_all('span')[1].text
    except AttributeError:
        owningTime = None

    try:
        pts = card_info.find('li', class_='CardInfoRow CardInfoRow_pts')
        pts = pts.find_all('span')[1].text
    except AttributeError:
        pts = None

    try:
        drive = card_info.find('li', class_='CardInfoRow CardInfoRow_drive')
        drive = drive.find_all('span')[1].text
    except AttributeError:
        drive = None

    try:
        wheel = card_info.find('li', class_='CardInfoRow CardInfoRow_wheel')
        wheel = wheel.find_all('span')[1].text
    except AttributeError:
        wheel = None

    try:
        state = card_info.find('li', class_='CardInfoRow CardInfoRow_state')
        state = state.find_all('span')[1].text
    except AttributeError:
        state = None

    try:
        customs = card_info.find(
            'li', class_='CardInfoRow CardInfoRow_customs')
        customs = customs.find_all('span')[1].text
    except AttributeError:
        customs = None

    try:
        transmission = card_info.find(
            'li', class_='CardInfoRow CardInfoRow_transmission')
        transmission = transmission.find_all('span')[1].text
    except AttributeError:
        transmission = None

    try:
        description = car['description']
    except KeyError:
        description = None

    body_type_human = car['vehicle_info']['configuration']['human_name']
    body_type = car['vehicle_info']['configuration']['body_type']
    eng_transmission = car['vehicle_info']['tech_param']['transmission']
    engine_volume = car['vehicle_info']['tech_param']['displacement']
    engine_volume = round(float(engine_volume) / 1000, 1)

    car_dict = {'bodyType': body_type_human, 'brand': brand, 'car_url': car_url, 'color': color,
                'complectation_dict': car['vehicle_info']['complectation'], 'description': description,
                'engineDisplacement': str(engine_volume) + ' LTR',
                'enginePower': str(car['vehicle_info']['tech_param']['power']) + ' N12',
                'equipment_dict': car['vehicle_info']['equipment'],
                'fuelType': fuelType, 'image': 'https:' + car['state']['image_urls'][0]['sizes']['small'],
                'mileage': car['state']['mileage'], 'modelDate': car['vehicle_info']['super_gen']['year_from'],
                'model_info': car['vehicle_info']['model_info'], 'model_name': model,
                'name': car['vehicle_info']['tech_param']['human_name'],
                'numberOfDoors': car['vehicle_info']['configuration']['doors_count'],
                'parsing_unixtime': round(time.time()), 'priceCurrency': 'RUB',
                'productionDate': car['documents']['year'], 'sell_id': car['id'],
                'super_gen': car['vehicle_info']['super_gen'],
                'vehicleConfiguration': body_type + " " + eng_transmission + " " + str(engine_volume),
                'vehicleTransmission': transmission, 'vendor': car['vehicle_info']['vendor'],
                'Владельцы': ownersCount, 'Владение': owningTime, 'ПТС': pts, 'Привод': drive, 'Руль': wheel,
                'Состояние': state, 'Таможня': customs, 'price': price}

    return car_dict


if __name__ == '__main__':
    cars_lst = []
    for brand in tqdm(brands_list, desc='Brands'):
        max_page = get_max_page(brand)
        for page in tqdm(range(1, max_page + 1),
                         leave=False,
                         desc='Pages'):
            param = get_param(brand, page)
            headers = get_headers(brand, page)
            cars = get_json(param, headers)
            with Pool() as p:
                cars_lst += p.map(get_car_dict, cars)

    cars_df = pd.DataFrame([car for car in cars_lst if car])
    filename = f'autoru-{date.today()}-parsingdate.csv'
    cars_df.to_csv(filename, index=False)
