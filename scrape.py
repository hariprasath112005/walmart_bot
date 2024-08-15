# from selenium import webdriver # type: ignore
# from selenium.webdriver.common.keys import Keys  # type: ignore
# import pandas as pd

# df = pd.DataFrame(columns=['data'])

# driver = webdriver.Chrome("/home/sams3pi0l/Downloads/chrome-linux64")
# driver.get("https://www.walmart.com/help/article/track-your-order/143cf6e1d8cb48e6a1ed840409881235")

# data = driver.find_elements_by_xpath("//article[@role='presentation']")

# data_list = []
# for i in range(len(data)):
#     data_list.append(data[i].text)


# data_tuples = list(zip(data_list[1:]))
# temp_df = pd.DataFrame(data_tuples, columns=['data'])
# df = df.append(temp_df)

# driver.close()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Set up the WebDriver (adjust the path to where you have the ChromeDriver)
service = Service('/home/sams3pi0l/Downloads/chrome/chromedriver-linux64/chromedriver')
driver = webdriver.Chrome(service=service)

# Navigate to the Walmart Help page
url = "https://www.walmart.com/help"
driver.get(url)

# Wait for the page to load fully (adjust the sleep time as needed)
time.sleep(50)

# Example: Expand all FAQ sections (if needed)
try:
    expand_buttons = driver.find_elements(By.CLASS_NAME, "accordion__title")
    for button in expand_buttons:
        driver.execute_script("arguments[0].click();", button)
        time.sleep(1)  # Add a small delay between clicks
except Exception as e:
    print("Error expanding FAQ sections:", e)

# Scrape the FAQ data
faq_data = []
faq_sections = driver.find_elements(By.CLASS_NAME, "accordion__section")

for section in faq_sections:
    try:
        question = section.find_element(By.CLASS_NAME, "accordion__title").text.strip()
        answer = section.find_element(By.CLASS_NAME, "accordion__content").text.strip()
        faq_data.append({"Question": question, "Answer": answer})
    except Exception as e:
        print(f"Error scraping section: {e}")

# Close the WebDriver
driver.quit()

# Convert the data to a DataFrame and save to CSV
df = pd.DataFrame(faq_data)
df.to_csv("walmart_faqs.csv", index=False)

print("Scraping completed and data saved to walmart_faqs.csv")
