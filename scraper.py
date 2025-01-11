import requests
from bs4 import BeautifulSoup
import json
import os  # For checking if the file exists

websites = [
    "https://www.w3schools.com/html/html_forms.asp"
]
output_file = "scraped_data_with_parameters.json"

# Function to load existing data from the JSON file
def load_existing_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []  # Return an empty list if the file does not exist

# Function to save data back to the JSON file
def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Scraping function
def scrape_static(url, existing_data):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        print(f"Scraping {url} - Status Code: {response.status_code}")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract form details
        forms = []
        all_parameters = set()  # Use a set to avoid duplicate parameters
        for form in soup.find_all("form"):
            parameters = [input_tag.get("name") for input_tag in form.find_all("input") if input_tag.get("name")]
            all_parameters.update(parameters)
            form_details = {
                "action": form.get("action"),
                "method": form.get("method"),
                "parameters": parameters
            }
            forms.append(form_details)

        # Extract link details
        links = []
        for link in soup.find_all("a"):
            link_details = {
                "text": link.get_text(strip=True),
                "href": link.get("href")
            }
            links.append(link_details)

        # Update existing data
        for page_data in existing_data:
            if page_data["url"] == url:
                # Merge forms
                page_data["forms"].extend(forms)
                # Merge parameters (avoid duplicates)
                page_data["parameters"] = list(set(page_data["parameters"]).union(all_parameters))
                # Merge links
                page_data["links"].extend(links)
                break
        else:
            # If the URL is not already in the existing data, add a new entry
            existing_data.append({
                "url": url,
                "forms": forms,
                "parameters": list(all_parameters),
                "links": links
                
            })

    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Load existing data
existing_data = load_existing_data(output_file)

# Scrape all websites and update the data
for website in websites:
    scrape_static(website, existing_data)

# Save the updated data back to the file
save_data(output_file, existing_data)
print(f"Scraping completed. Data updated in {output_file}.")
