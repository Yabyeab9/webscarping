#Importing libraries
import random
from bs4 import BeautifulSoup
import requests
import pandas as pd
quote =[]
author = []
link = []
url = "https://quotes.toscrape.com/"
request = requests.get(url).text
soup = BeautifulSoup(request,"html.parser")

container = soup.find_all("div", class_="quote")
for i in container:
    text = i.find("span", class_="text").text
    quote.append(text)
    Author = i.find("small", class_="author").text
    author.append(Author)
    link1 = url + i.find("a")["href"]
    link.append(link1)
data = {
    "Quote":quote,
    "Author":author,
    "Link": link
}
i = range(len(quote))
chance = 2
rand = (random.choice(i))
print(quote[rand])
#This is a sample game that some one guess the author of the quote the qoute get from https://quotes.toscrape.com/
ans = input("Enter the author of the above quote:  ")
while chance >0:
    if ans==author[rand]:
        print("Correct")
    else:
        chance-=1
        if chance==1:
            new_req = requests.get(link[rand]).text
            soup1 = BeautifulSoup(new_req,"html.parser")
            brith = soup1.find("span", class_="author-born-date").text
            location = soup1.find("span", class_="author-born-location").text
            print(f"Hint:)\n The birth year is {brith}\nThe birth location is{location}")
            if ans == author[rand]:
                print("Correct")
            else:
                print("Try again later!")




