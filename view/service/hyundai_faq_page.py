import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

chrome_options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.hyundai.com/kr/ko/e/customer/center/faq")

time.sleep(3)

output_file = "data.raw.hyundai_faq_data.csv"
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Category", "Question", "Answer"])

    try:
        categories = driver.find_elements(By.CSS_SELECTOR, "ul.tab-menu__icon-wrapper > li")
        print(f"Found {len(categories)} categories.")

        for category_index, category in enumerate(categories):
            category_name = category.text.strip()
            print(f"\nClicking on category {category_index + 1}/{len(categories)}: {category_name}")

            driver.execute_script("arguments[0].click();", category)
            time.sleep(3)

            try:
                questions = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.list-wrap > div"))
                )
                print(f"Found {len(questions)} questions in category '{category_name}'.")

                for question_index, question in enumerate(questions):

                    question_button = question.find_element(By.CSS_SELECTOR, "button.list-title")
                    question_text = question_button.text.strip()

                    driver.execute_script("arguments[0].click();", question_button)
                    time.sleep(2)

                    try:
                        answer = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.conts"))
                        ).text.strip()
                    except Exception as e:
                        answer = "No answer found"

                    print(f"  ({question_index + 1}/{len(questions)}) Question: {question_text}")
                    print(f"      Answer: {answer}")

                    writer.writerow([category_name, question_text, answer])

            except Exception as e:
                print(f"No questions found in category '{category_name}': {e}")

    except Exception as e:
        print(f"Error while processing the FAQ page: {e}")

    finally:
        driver.quit()

print(f"FAQ data has been saved to '{output_file}'.")
