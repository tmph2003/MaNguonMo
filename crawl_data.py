from lxml import html
import requests
import datetime as dt
import time
import random
import pandas as pd

class Crawl:
    def __init__(self) -> None:
        pass
    # def main(self):
    #     url = "https://www.binance.com/vi/markets/overview"
    #     data = []
    #     response = requests.get(url=url)
    #     tree = html.fromstring(response.content)
    #     datetime_now = dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    #     for i in range(1, 11):
    #         temp = {
    #             'name': dict(),
    #             'price': dict(),
    #             'datetime': dict()
    #         }
    #         xpath1 = f"//*[@id='tabContainer']/div[2]/div[3]/div/div/div[2]/div[{i}]/div/div[1]/text()"
    #         xpath2 = f"//*[@id='tabContainer']/div[2]/div[3]/div/div/div[2]/div[{i}]/div/a/div/div/div[2]/div[2]/text()"
    #         price = tree.xpath(xpath1)[0][1:]
    #         name = tree.xpath(xpath2)[0]
    #         temp["name"] = name
    #         temp["price"] = price
    #         temp["datetime"] = datetime_now
    #         data.append(temp)
    #     return data
    def main(self, data):
        temp = []
        temp.append(float(data[b'Price:Open'].decode('utf-8')))
        temp.append(float(data[b'Price:High'].decode('utf-8')))
        temp.append(float(data[b'Price:Low'].decode('utf-8')))
        temp.append(float(data[b'Price:Close'].decode('utf-8')))
        random_values = [random.randint(0, 1) for _ in range(4)]
        for i in range(4):
            if random_values[i] == 0:
                temp[i] += random.randint(0, 100)
            else:
                temp[i] -= random.randint(0, 100)
        return temp


if __name__ == "__main__":
    crawl = Crawl()
    data = crawl.main({b'Date:': b'2023-07-20', b'Price:Close': b'30189.902344', b'Price:High': b'30224.115234', b'Price:Low': b'29918.281250', b'Price:Open': b'29919.064453'})
    print(data)