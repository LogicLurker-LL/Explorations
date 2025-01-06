import requests  # static scrapping uses requests and beutiful soap to extyract form details
from bs4 import BeautifulSoup
import pandas as pd

websites = [
    "https://www.w3schools.com/html/html_forms.asp"
    
]
scraped_data = []

def scrape_static(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}) #User-Agent is set to mimic a browser and avoid getting blocked
        print(f"Scraping {url} - Status Code: {response.status_code}")
        if response.status_code != 200:
            print("Failed to retrieve the webpage.")

        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract form details
        forms = soup.find_all("form")
        for form in forms:
            form_details = {
                "URL": url,
                "Form Action": form.get("action"),
                "Method": form.get("method"),
                "Input Fields": [input_tag.get("name") for input_tag in form.find_all("input")]
            }
            print(f"Scraped form: {form_details}")
            scraped_data.append(form_details)
        
        # Scrape all links on the page
        links = soup.find_all("a")
        print(f"Found {len(links)} links on {url}")

        for link in links:
            link_details = {
                "URL": url,
                "Link Text": link.get_text(strip=True),  # Text inside the link
                "Link URL": link.get("href")  # URL the link points to
            }
            print(f"Scraped link: {link_details}")
            scraped_data.append(link_details)

            print(f"Found {len(forms)} forms on {url}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")

    
for website in websites:
    print(f"Scraping {website}...")
    # First, try static scraping
    scrape_static(website)


output_file = "scraped_data.csv"
df = pd.DataFrame(scraped_data)
df.to_csv(output_file, index=False)
print(f"Scraping completed. Data saved to {output_file}.")