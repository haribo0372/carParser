import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint


def get_param_auto_ru(data):
    for key, value in data.items():
        data[key] = value.lower().strip()

    if data["min_power"] != "":
        data["min_power"] = str(int(float(data["min_power"]) * 1000))

    if data["max_power"] != "":
        data["max_power"] = str(int(float(data["max_power"]) * 1000))

    auto_ru_parametres = {"mark": "brand",
                          "model": "model",
                          "generation": "generation",
                          "body_type_group": "car_body",
                          "transmission": "shift_box",
                          "gear_type": "privod",
                          "engine_group": "fuel",
                          "displacement_from": "min_power",
                          "displacement_to": "max_power",
                          "year_from": "min_year",
                          "year_to": "max_year",
                          "km_age_from": "min_probeg",
                          "km_age_to": "max_probeg",
                          "price_from": "min_price",
                          "price_to": "max_price",
                          "color": "colour",
                          "steering_wheel": "wheel"
                          }
    parameteres = {
        "body_type_group": {
            "седан": "SEDAN",
            "хэтчбек 5дв": "HATCHBACK_5_DOORS",
            "хэтчбек 3ДВ": "HATCHBACK_3_DOORS",
            "лифтбек": "LIFTBACK",
            "джип 5 дв": "ALLROAD_5_DOORS",
            "джип 3 дв": "ALLROAD_3_DOORS",
            "универсал": "WAGON",
            "минивен": "MINIVAN",
            "пикап": "PICKUP",
            "купе": "COUPE",
            "открытый": "CABRIO"
        },
        "transmission": {
            "механика": "MECHANICAL",
            "акпп": "AUTOMATIC",
            "робот": "ROBOT",
            "вариатор": "VARIATOR",
            "автомат": "AUTO"
        },
        "engine_group": {
            "бензин": "GASOLINE",
            "дизель": "DIESEL",
            "электро": "HYBRID",
            "гибрид": "ELECTRO",
            "гбо": "LPG"
        },
        "gear_type": {
            "передний": "FORWARD_CONTROL",
            "задний": "REAR_DRIVE",
            "полный": "ALL_WHEEL_DRIVE"
        },
        "color": {
            "белый": "FAFBFB",
            "черный": "040001",
            "коричневый": "200204",
            "фиолетовый": "4A2197",
            "зелёный": "007F00",
            "синий": "0000CC",
            "голубой": "22A0F8",
            "серый": "97948F",
            "серебристый": "CACECB",
            "бежевый": "C49648",
            "жёлтый": "FFD600",
            "золотистый": "DEA522",
            "красный": "EE1D19",
            "бордовый": "660099",
            "оранжевый": "FF8649",
            "рыжий": "FF8649",
        },
        "steering_wheel": {
            "левый": "LEFT",
            "правый": "RIGHT"
        }
    }
    for key, value in auto_ru_parametres.items():
        if data[value] == "":
            auto_ru_parametres[key] = None
        elif key in ["body_type_group", "transmission", "engine_group", "gear_type", "color", "steering_wheel"]:
            auto_ru_parametres[key] = parameteres[key][data[value]]
        else:
            auto_ru_parametres[key] = data[value]

    return auto_ru_parametres


def get_content_auto_ru(html_text: str) -> list:
    data = []
    soup = BeautifulSoup(html_text, "lxml").find_all("div", class_="ListingItem")

    for i in soup:
        name = i.find("a", class_="Link ListingItemTitle__link").text
        href = i.find("a", class_="Link ListingItemTitle__link").get("href")

        price = i.find("div", class_="ListingItem__priceBlock").find_next().find_next()
        price_mb = i.find("div", class_="ListingItem__price_second")
        if price_mb is not None:
            price = price.text + " " + price_mb.text
        else:
            price = price.text
        price = price.replace('\xa0', ' ')

        parameters = []
        soup_parameters = i.find_all("div", class_="ListingItemTechSummaryDesktop__column")
        for j in soup_parameters:
            parameters_block = j.find_all("div", class_="ListingItemTechSummaryDesktop__cell")
            for k in parameters_block:
                parameters.append(k.text.replace("\u2009/\u2009", "/").replace('\xa0', ''))

        city = i.find("div", class_="ListingItem__placeBlock").find("span", class_="MetroListPlace__regionName").text.replace('\xa0', ' ')

        car = [name, price, parameters, city, href]

        data.append(car)

    return data


def count_auto(html_text):
    soup = BeautifulSoup(html_text, "lxml").find("div", class_="ListingCarsFilters__actions")
    soup = soup.find("button", class_="Button Button_color_blue Button_size_m Button_type_button Button_width_full")
    soup = soup.find_next().find_next().text
    count = ""
    for i in soup:
        print(i, end="")



def get_html_auto_ru(params: dict, session) -> str:
    COOKIE = 'вставь свое!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    HEADERS = {
        'user-agent': 'встав свое !!!!!!!!!!!',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru',
        'accept-encoding': 'accept - encoding: gzip, deflate, br',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Opera";v="87"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': COOKIE
    }

    url = "https://auto.ru/moskva/cars/all/"

    req = session.get(url, headers=HEADERS, params=params)

    req.encoding = 'utf-8'

    html_txt = req.text

    return html_txt


def parser_auto_ru(data):
    cars = []
    page = 0
    params = get_param_auto_ru(data)
    session = requests.Session()
    scr = get_html_auto_ru(params, session)
    print(count_auto(scr))
    while True:
        params["page"] = page
        page += 1
        scr = get_html_auto_ru(params, session)
        pause = randint(100000, 200000) / 100000
        sleep(pause)
        car = get_content_auto_ru(scr)
        print(car)
        if len(car) == 0:
            session.close()
            break
        else:
            cars += car

    for i in range(len(cars)):
        print(i + 1, cars[i])


data_car = {
    "brand": "bmw",
    "model": "",
    "generation": "",
    "restyling": "",
    "car_body": "седан",
    "min_price": "",
    "max_price": "",
    "min_year": "",
    "max_year": "",
    "shift_box": "",
    "fuel": "",
    "min_power": "",
    "max_power": "",
    "privod": "",
    "colour": "",
    "wheel": "",
    "min_probeg": "",
    "max_probeg": ""
}

parser_auto_ru(data_car)