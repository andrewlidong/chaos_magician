import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# LinkedIn login credentials
LINKEDIN_USERNAME = 'your_email@example.com'
LINKEDIN_PASSWORD = 'your_password'

# List of companies to search for
companies = [
    "Tonal",
    "Chainalysis",
    "Roboflow",
    "Anthropic",
    "Frontegg",
    "Deepgram"
]

# Initialize WebDriver
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
service = Service('/path/to/chromedriver')  # Ensure chromedriver is in your PATH
driver = webdriver.Chrome(service=service, options=chrome_options)

def linkedin_login():
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)

    username_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')
    sign_in_button = driver.find_element(By.XPATH, '//*[@type="submit"]')

    username_field.send_keys(LINKEDIN_USERNAME)
    password_field.send_keys(LINKEDIN_PASSWORD)
    sign_in_button.click()
    time.sleep(5)

def search_heads_of_sre(company):
    search_query = f"Head of SRE at {company}"
    search_box = driver.find_element(By.XPATH, '//input[contains(@class, "search-global-typeahead__input")]')
    search_box.clear()
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

    # Scroll to load more results
    for _ in range(5):
        ActionChains(driver).send_keys(Keys.END).perform()
        time.sleep(2)

    profiles = driver.find_elements(By.XPATH, '//a[contains(@class, "app-aware-link")]')

    results = []
    for profile in profiles:
        name = profile.find_element(By.XPATH, './/span[contains(@class, "actor-name")]').text
        profile_link = profile.get_attribute('href')
        results.append([name, profile_link])

    return results

def save_to_csv(company, data):
    filename = f"{company}_Heads_of_SRE.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Profile Link"])
        writer.writerows(data)

def main():
    linkedin_login()
    
    for company in companies:
        results = search_heads_of_sre(company)
        save_to_csv(company, results)

    driver.quit()

if __name__ == "__main__":
    main()

