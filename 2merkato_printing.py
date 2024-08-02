from bs4 import BeautifulSoup
import requests
import pandas as pd
import schedule
import time

def scrape_data():
    url = "https://www.2merkato.com/directory/401/page:12"
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")


    Name_of_company = []
    commpany_element = soup.find_all("div", "span12 heading")
    phone_num = []
    Location = []
    # Fetching name of the company
    for commpany_names in commpany_element:
        name = commpany_names.text.strip()  
        Name_of_company.append(name)
        # Fetching other details about the company
        links = commpany_names.find_all("a")
        for l in links:
            full_link = "https://www.2merkato.com" + l.get("href")
            page_response = requests.get(full_link)
            soup2 = BeautifulSoup(page_response.text,"html.parser")
            tables = soup2.find_all("table", "table table-condensed")
            company_phone_numbers = []
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) == 2:
                        label = cells[0].text.strip()
                        value = cells[1].text.strip()
                        if label == "Location":
                            Location.append(value)
                        elif label == "Phone" or label == "Phone 2" or label == "Mobile":
                            company_phone_numbers.append(value)
            phone_num.append(company_phone_numbers)

    data={
        "Company name":Name_of_company,
        "Phone number": phone_num,
        "Location": Location
    }
  
    df = pd.DataFrame(data)

    try:
        # Load the existing CSV file
        existing_df = pd.read_csv("Agent.csv")
        # Check if there are any new rows(Check by the company name)
        #If there is new data (not new_rows.empty) = True
        new_rows = df[~df["Company name"].isin(existing_df["Company name"])]
        if not new_rows.empty:
            print("New data added to the CSV file:")
            print(new_rows)
            # The new data will concatenate with the existing data
            existing_df = pd.concat([existing_df, new_rows], ignore_index=True)
            existing_df.to_csv("Agent.csv", index=False)
        else:
            print("No new data to add.")
    except FileNotFoundError:
        # If the CSV file doesn't exist, create a new one
        df.to_csv("Agent.csv", index=False)
        print("CSV file created.")

# Schedule the scrape_data function to run every 24 hours
schedule.every(24).hours.do(scrape_data)

while True:
    #Execute the scheduled function  
    schedule.run_pending()
    time.sleep(1)