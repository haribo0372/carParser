import requests
from bs4 import BeautifulSoup


def get_html_drom(url: str) -> str:
    html_text = requests.get(url).text
    return html_text


def get_content_drom(scr: str) -> list:
    try:
        data = []
        soup = BeautifulSoup(scr, "lxml").find("div", class_="css-1nvf6xk")
        if soup is not None:
            soup = soup.find_all("a", class_="css-xb5nz8 e1huvdhj1")
            for i in soup:
                href = i.get("href").strip()
                name = i.find("div", class_="css-l1wt7n e3f4v4l2").find("span").text

                specifications = i.find("div", class_="css-1fe6w6s e162wx9x0").find_all("span")
                parameters = ""
                for parameter in specifications:
                    parameters += parameter.text + " "

                price = i.find("span", class_="css-46itwz e162wx9x0").find("span").text.strip().replace("\xa0",
                                                                                                        " ") + "₽"
                city = i.find("div", class_="css-1x4jcds eotelyr0").find("span").text.strip()
                car = [href, name, parameters, price, city]

                data.append(car)
                print(car)
        return data
    except:
        print("Ошибка при сборе данных в дром")
        return []


def parser_drom():
    url = "скопируй url машины !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    data = []
    page = 0
    while True:
        url = url.replace(f"page{page}", f"page{page + 1}")
        page += 1
        scr = get_html_drom(url)
        print(scr)
        car_blok = get_content_drom(scr)
        if not car_blok:
            break
        else:
            data += car_blok

    for i in range(len(data)):
        print(i + 1, data[i])


parser_drom()
