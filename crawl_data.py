from lxml import html
import requests
import datetime as dt
import time

class Crawl:
    def __init__(self) -> None:
        pass
    def main(self):
        url = "https://www.binance.com/vi/markets/overview"
        data = []
        response = requests.get(url=url)
        tree = html.fromstring(response.content)
        datetime_now = dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        for i in range(1, 11):
            temp = {
                'name': dict(),
                'price': dict(),
                'datetime': dict()
            }
            xpath1 = f"//*[@id='tabContainer']/div[2]/div[3]/div/div/div[2]/div[{i}]/div/div[1]/text()"
            xpath2 = f"//*[@id='tabContainer']/div[2]/div[3]/div/div/div[2]/div[{i}]/div/a/div/div/div[2]/div[2]/text()"
            price = tree.xpath(xpath1)[0][1:]
            name = tree.xpath(xpath2)[0]
            temp["name"] = name
            temp["price"] = price
            temp["datetime"] = datetime_now
            data.append(temp)
        return data

if __name__ == "__main__":
    while True:
        crawl = Crawl()
        data = crawl.main()
        print(data)
        time.sleep(120)