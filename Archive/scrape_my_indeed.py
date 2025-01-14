from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

# Set up Selenium WebDriver (ensure you have the ChromeDriver or another driver installed)
driver = webdriver.Chrome()  # Or use webdriver.Firefox() if using Firefox
driver.maximize_window()

# Step 1: Log in to Indeed
driver.get("https://secure.indeed.com/account/login")

# Wait for the page to load (adjust sleep time if needed)
time.sleep(5)

# Enter your credentials (manually or with environment variables for security)
email = driver.find_element(By.ID, "login-email-input")
password = driver.find_element(By.ID, "login-password-input")

email.send_keys("your_email@example.com")
password.send_keys("your_password")
password.send_keys(Keys.RETURN)

# Wait for the login to complete and redirect to the saved jobs page
time.sleep(10)

# Step 2: Navigate to saved jobs
driver.get("https://myjobs.indeed.com/saved")
time.sleep(5)

# Step 3: Extract job details
job_list = []
jobs = driver.find_elements(By.CSS_SELECTOR, "div.job_card_class")  # Adjust the selector as needed

for job in jobs:
    title = job.find_element(By.CSS_SELECTOR, "h2").text
    company = job.find_element(By.CSS_SELECTOR, ".company_name_class").text
    location = job.find_element(By.CSS_SELECTOR, ".location_class").text
    job_list.append({"title": title, "company": company, "location": location})

# Step 4: Remove duplicates
unique_jobs = {f"{job['title']}|{job['company']}": job for job in job_list}.values()

# Step 5: Save to CSV
with open("saved_jobs.csv", "w", newline="") as csvfile:
    fieldnames = ["title", "company", "location"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(unique_jobs)

print("Saved jobs exported to saved_jobs.csv")

# Close the browser
driver.quit()