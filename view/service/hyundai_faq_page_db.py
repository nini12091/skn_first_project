from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import mysql.connector
import time

# MySQL Database Connection
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="carsystemdb"
)
cursor = connection.cursor()

chrome_options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.hyundai.com/kr/ko/e/customer/center/faq")

time.sleep(3)

# List to store scraped data
scraped_data = []

try:
    # Scraping logic
    list_elements = driver.find_elements(By.CSS_SELECTOR, "ul.tab-menu__icon-wrapper > li > button")

    for index, element in enumerate(list_elements):
        category_name = element.text.strip()
        print(f"Clicking on category {index + 1}: {category_name}")

        # Click category
        driver.execute_script("arguments[0].scrollIntoView(true);", element)  # Scroll
        time.sleep(1)
        driver.execute_script("arguments[0].click();", element)  # Click

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.active"))
        )

        # Reset to the first page (if applicable)
        try:
            first_page_button = driver.find_element(By.CSS_SELECTOR, "ul.el-pager li.number:first-child button")
            driver.execute_script("arguments[0].click();", first_page_button)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-item"))
            )
            time.sleep(2)
        except Exception as e:
            print(f"Failed to reset to the first page: {e}")

        # Pagination handling
        while True:
            try:
                # Extract FAQ items
                faq_items = driver.find_elements(By.CSS_SELECTOR, "div.list-item")
                for faq_item in faq_items:
                    try:
                        question_element = faq_item.find_element(By.CSS_SELECTOR, "div.title")
                        question = question_element.text.strip() if question_element else "No question found"

                        # Expand the answer
                        driver.execute_script("arguments[0].click();", question_element)
                        time.sleep(1)

                        answer_element = faq_item.find_element(By.CSS_SELECTOR, "div.conts")
                        answer = answer_element.text.strip() if answer_element else "No answer found"

                        print(f"Extracted - Brand: hyundai, Category: {category_name}, Question: {question}, Answer: {answer}")

                        # Save to list
                        scraped_data.append({
                            "brand": "hyundai",
                            "category": category_name,
                            "question": question,
                            "answer": answer
                        })

                        # Insert into MySQL database
                        cursor.execute("""
                        INSERT INTO faq_data (brand, category, question, answer) 
                        VALUES (%s, %s, %s, %s)
                        """, ("hyundai", category_name, question, answer))
                        connection.commit()

                    except Exception as e:
                        print(f"Failed to extract question/answer: {e}")

                # Pagination
                pagination_buttons = driver.find_elements(By.CSS_SELECTOR, "ul.el-pager li.number button")

                active_page_index = driver.find_element(By.CSS_SELECTOR, "ul.el-pager li.number.active button").text.strip()

                if int(active_page_index) < len(pagination_buttons):
                    # Click next page
                    next_button = pagination_buttons[int(active_page_index)]  # Pages are 0-indexed
                    driver.execute_script("arguments[0].click();", next_button)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-item"))
                    )
                    time.sleep(2)
                else:
                    break  # No more pages
            except Exception as e:
                print(f"Failed to navigate pagination: {e}")
                break

except Exception as e:
    print(f"Error while processing the list: {e}")

finally:
    driver.quit()
    cursor.close()
    connection.close()
    print("Scraping completed and saved to database.")

