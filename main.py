import requests
import unicodedata
from bs4 import BeautifulSoup


def get_html_code(url: str) -> str:
    html_text = requests.get(url).text
    return html_text


def get_drom(html_code: str):
    try:
        data = []
        soup = BeautifulSoup(htmlz_code, "html.parser").find("div", class_="css-1nvf6xk")
        if soup is not None:
            soup = soup.findAll('a', class_='css-xb5nz8 e1huvdhj1')
            for i in soup:

                href = i.get('href').strip()
                name = i.find('div', class_='css-l1wt7n e3f4v4l2').find('span').text
                specifications = i.find("div", class_="css-1fe6w6s e162wx9x0").find_all("span")
                parametrs = ""
                for parametr in specifications:
                    parametrs += parametr.text + " "
                parametrs = unicodedata.normalize("NFKD", parametrs)
                price = unicodedata.normalize("NFKD", i
                                              .find("span", class_="css-46itwz e162wx9x0")
                                              .find("span").text.strip() + "₽")
                city = i.find("div", class_="css-1x4jcds eotelyr0").find("span").text.strip()
                car = [href, name, parametrs, price, city]
                data.append(car)
                print(car)
        return data
    except:
        print("Ошибка при сборе данных в дром")
        return []


def get_full_info():
    data = []
    url = "https://moscow.drom.ru/toyota/all/?maxprice=1000000"
    get_drom(url)
    page = 0
    while True:
        url = url.replace(f"page{page}", f"page{page + 1}")
        page += 1
        htmlCode = get_html_code(url)
        info = get_drom(htmlCode)
        if not info:
            break
        else:
            data += info


get_full_info()
