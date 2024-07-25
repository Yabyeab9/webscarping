from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

price_list = []
address_list = []
description_list = []


url = "https://jiji.com.et/addis-ababa/houses-apartments-for-rent?price_max=15000"
response = requests.get(url).text
soup =BeautifulSoup (response, "html.parser")
body = soup.find_all("div", class_="masonry-item")

for i in body:
    price = i.find("div",class_="qa-advert-price").text.strip()
    price_list.append(price)
    address = i.find("span", class_="b-list-advert__region__text").text.strip()
    address_list.append(address)
    des= i.find("div", class_="b-advert-title-inner qa-advert-title b-advert-title-inner--div").text.strip()
    description_list.append(des)

data={
    "Price": price_list,
    "Address": address_list,
    "Description": description_list
}
df = pd.DataFrame(data)
df.to_csv("Sample.csv",index=False)

print("Done")

