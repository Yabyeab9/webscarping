from bs4 import BeautifulSoup
import requests
import pandas as pd
import schedule
import time

def scrape_data():
    data = {
        "Company name": [],
        "Phone number": [],
        "Location": []
    }

    for i in range(2, 14):
        url = f"https://www.2merkato.com/directory/459/page:{i}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        company_elements = soup.find_all("div", "span12 body")
        a_tags = []
        company_phone_numbers = [] 
        location= []
        phone_num=[]
        Name_of_company = []
        #Fetching a data that are more illustrated like they have detail about the location
        if company_elements:
            for company_element in company_elements:
                name = company_element.text.strip()
                data["Company name"].append(name)
                
                company_phone_numbers = []
                location = None
                h5_links = company_element.find_all("h5")
                for link in h5_links:
                    a_tags = link.find_all("a")
        else:
            #Fetching data that have only company name and link to see the detail
            commpany_element = soup.find_all("div", "span12 heading")
            # Fetching name of the company
            for commpany_names in commpany_element:
                name = commpany_names.text.strip()  
                Name_of_company.append(name)
                # Fetching other details about the company
                a_tags = commpany_names.find_all("a")
        for a in a_tags:
            full_link = "https://www.2merkato.com" + a.get("href")
            page_response = requests.get(full_link)
            soup2 = BeautifulSoup(page_response.text, "html.parser")
            tables = soup2.find_all("table", "table table-condensed")
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) == 2:
                        label = cells[0].text.strip()
                        value = cells[1].text.strip()
                        if label == "Location":
                            location.append(label)
                        elif label == "Phone" or label == "Phone 2" or label == "Mobile":
                            company_phone_numbers.append(value)
            phone_num.append(company_phone_numbers)
    data = {
        "Name": Name_of_company,
        "Number": phone_num,
        "Location": location
    }

    df = pd.DataFrame(data)
 

    try:
        # Load the existing CSV file
        existing_df = pd.read_csv("Hotel.csv")
        # Check if there are any new rows(Check by the company name)
        new_rows = df[~df["Company name"].isin(existing_df["Company name"])]
        if not new_rows.empty:
            print("New data added to the CSV file:")
            print(new_rows)
            # The new data will concatenate with the existing data
            existing_df = pd.concat([existing_df, new_rows], ignore_index=True)
            existing_df.to_csv("Hotel.csv", index=False)
        else:
            print("No new data to add.")
    except FileNotFoundError:
        # If the CSV file doesn't exist, create a new one
        df.to_csv("Hotel.csv", index=False)
        print("CSV file created.")


#Schedule the scrape_data function to run every 24 hours
schedule.every(24).hours.do(scrape_data)

while True:
    #Execute the scheduled function  
    schedule.run_pending()
    time.sleep(1)