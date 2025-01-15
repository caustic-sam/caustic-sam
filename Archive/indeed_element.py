import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/chromium-browser"

# Specify the path to chromedriver
chromedriver_path = '/usr/local/bin/chromedriver'
service = Service(chromedriver_path)

# List of common elements to check
elements_to_check = [
    (By.ID, "login-email-input"),
    (By.ID, "username"),
    (By.NAME, "email"),
    (By.TAG_NAME, "h1"),
    (By.TAG_NAME, "input"),
    (By.CLASS_NAME, "login-form"),
    (By.CLASS_NAME, "form-control"),
]

def main():
    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Open the Indeed login page
        driver.get("https://www.indeed.com/account/login")
        print("Opened Indeed login page.")
        
        # Wait for the page to load
        time.sleep(3)
        
        # Check for common elements
        for by, value in elements_to_check:
            try:
                element = driver.find_element(by, value)
                print(f"Element found: {by}='{value}'")
            except Exception as e:
                print(f"Element not found: {by}='{value}'")
        
    finally:
        # Close the browser
        driver.quit()
        print("Closed the browser.")

if __name__ == "__main__":
    main()