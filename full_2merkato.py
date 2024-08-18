import csv
from bs4 import BeautifulSoup
import pandas as pd
import requests

# first page
first_Page = 1
#lastpage
url = "https://www.2merkato.com/directory/"
response = requests.get(url).text
soup = BeautifulSoup(response,"html.parser")
link = soup.find("div",class_="pagination")
link_tag = link.find("a",{"title":"End"})
last_Page = int(link_tag["href"].split(':')[-1])
end_page = last_Page +1

Name_of_company = []
phone_num = []
location = []

for i in range(1,end_page):
    full_url = url +"page:"+str(i)
    response2 = requests.get(full_url).text
    soup2= BeautifulSoup(response2,"html.parser")
    company_elements = soup2.find_all("div","row-fluid")
    for company in company_elements:
        company_name = company.find("h4")
        if company_name:
            link = company_name.find("a")
            if link:
                name = link.text.strip()
                Name_of_company.append(name)
                full_link = "https://www.2merkato.com" + link.get("href")
                detail = requests.get(full_link).text
                soup3 = BeautifulSoup(detail, "html.parser")
                tables = soup3.find_all("table", "table table-condensed")
                company_phone_numbers = []
                company_location = []
                for table in tables:
                    rows = table.find_all("tr")
                    for row in rows:
                        cells = row.find_all("td")
                        if len(cells) == 2:
                            label = cells[0].text.strip()
                            value = cells[1].text.strip()
                            if label == "Location":
                                company_location.append(value)
                            elif label == "Phone" or label == "Phone 2" or label == "Mobile":
                                company_phone_numbers.append(value)
                phone_num.append(', '.join(company_phone_numbers))
                location.append(', '.join(company_location))

data = {
    "Name": Name_of_company,
    "Number": phone_num,
    "Location": location
}

df = pd.DataFrame(data)
df.to_csv("2merkato_data.csv",index=False)