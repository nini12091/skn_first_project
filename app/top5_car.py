import requests
from bs4 import BeautifulSoup
import re


def parse_car_data(raw_data):
    car_data = []
    lines = raw_data.split("​")

    brand_keywords = {
        "현대자동차": ["대표 모델", "설립", "본사", "홈페이지"],
        "기아": ["대표 모델", "설립", "본사", "홈페이지"],
        "한국지엠": ["대표 모델", "설립", "본사", "홈페이지"],
        "쌍용자동차": ["대표 모델", "설립", "본사", "홈페이지"],
        "르노코리아": ["대표 모델", "설립", "본사", "홈페이지"]
    }

    current_brand = None
    for line in lines:
        line = line.strip()

        for brand in brand_keywords.keys():
            if brand in line:
                current_brand = brand
                break

        if current_brand:
            for key in brand_keywords[current_brand]:
                if key in line:
                    if key == "대표 모델":
                        detail = line.split(":")[-1].strip()
                    elif key == "홈페이지":
                        urls = re.findall(r'https?://[^\s]+', line)
                        if urls:
                            detail = urls[0]
                            if "kia.com" in detail:
                                continue
                        else:
                            continue
                    else:
                        detail = line.replace("■", "").strip()

                    if not any(d['정보'] == key and d['내용'] == detail and d['브랜드'] == current_brand for d in car_data):
                        car_data.append({"브랜드": current_brand, "정보": key, "내용": detail})
    return car_data


def get_top_5_cars():
    url = "https://blog.naver.com/PostView.nhn?blogId=ahaeyam&logNo=223005461016"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.find('div', {'class': 'se-main-container'})
        if content:
            return content.get_text(strip=True)
        else:
            return "🚨 데이터를 찾을 수 없습니다."
    except requests.RequestException as e:
        return f"🚨 에러 발생: {e}"