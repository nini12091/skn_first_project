import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

import mysql.connector
import csv


connection = mysql.connector.connect(
    host="localhost",
    user='root',
    password='1234',
    database='carsystemdb'
)

cursor = connection.cursor()
csv_file = os.path.join(project_root, "data", "raw", "hyundai_faq.csv")
brand_name = "hyundai"

with open(csv_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        category = row[0]
        question = row[1]
        answer = row[2]

        cursor.execute("""
        INSERT INTO faq_data (brand, category, question, answer)
        VALUES (%s, %s, %s, %s)
        """, (brand_name, category, question, answer))

connection.commit()
print("CSV 데이터를 데이터베이스에 삽입했습니다.")

cursor.close()
connection.close()