from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import csv
import time

chrome_options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.hyundai.com/kr/ko/e/customer/center/faq")

time.sleep(3)

try:
    with open("../../data/raw/hyundai_faq.csv", mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)

        # CSV 파일 헤더 작성
        writer.writerow(["Brand", "Category", "Question", "Answer"])

        # 카테고리 버튼 탐색
        list_elements = driver.find_elements(By.CSS_SELECTOR, "ul.tab-menu__icon-wrapper > li > button")

        for index, element in enumerate(list_elements):
            category_name = element.text.strip()
            print(f"Clicking on category {index + 1}: {category_name}")

            # 카테고리 클릭
            driver.execute_script("arguments[0].scrollIntoView(true);", element)  # 스크롤
            time.sleep(1)
            driver.execute_script("arguments[0].click();", element)  # 클릭

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.active"))
            )

            # 페이지를 1로 초기화 (첫 페이지로 이동)
            try:
                first_page_button = driver.find_element(By.CSS_SELECTOR, "ul.el-pager li.number:first-child button")
                driver.execute_script("arguments[0].click();", first_page_button)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-item"))
                )
                time.sleep(2)
            except Exception as e:
                print(f"Failed to reset to the first page: {e}")

            # 페이지네이션 처리
            while True:
                try:
                    # 현재 페이지에서 FAQ 아이템 추출
                    faq_items = driver.find_elements(By.CSS_SELECTOR, "div.list-item")
                    for faq_item in faq_items:
                        try:
                            question_element = faq_item.find_element(By.CSS_SELECTOR, "div.title")
                            question = question_element.text.strip() if question_element else "No question found"

                            # 답변 펼치기
                            driver.execute_script("arguments[0].click();", question_element)
                            time.sleep(1)

                            answer_element = faq_item.find_element(By.CSS_SELECTOR, "div.conts")
                            answer = answer_element.text.strip() if answer_element else "No answer found"

                            print(f"Extracted - Brand: hyundai, Category: {category_name}, Question: {question}, Answer: {answer}")

                            # 데이터 저장
                            writer.writerow(["hyundai", category_name, question, answer])
                        except Exception as e:
                            print(f"Failed to extract question/answer: {e}")

                    # 페이지네이션 버튼 새로 가져오기
                    pagination_buttons = driver.find_elements(By.CSS_SELECTOR, "ul.el-pager li.number button")

                    # 현재 활성화된 페이지 탐색
                    active_page_index = driver.find_element(By.CSS_SELECTOR, "ul.el-pager li.number.active button").text.strip()

                    # 다음 페이지가 있는지 확인
                    if int(active_page_index) < len(pagination_buttons):
                        # 다음 페이지 클릭
                        next_button = pagination_buttons[int(active_page_index)]  # 현재 페이지는 0부터 시작
                        driver.execute_script("arguments[0].click();", next_button)
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div.list-item"))
                        )
                        time.sleep(2)
                    else:
                        break  # 더 이상 페이지 없음
                except Exception as e:
                    print(f"Failed to navigate pagination: {e}")
                    break

except Exception as e:
    print(f"Error while processing the list: {e}")

finally:
    driver.quit()
    print("Scraping completed and saved to hyundai_faq.csv.")
