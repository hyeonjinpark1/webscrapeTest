from playwright.sync_api import sync_playwright
import math
import pandas as pd

def fetch_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 브라우저 비활성화 모드
        page = browser.new_page()

        # URL 설정
        base_url = "https://www.murata.com/search/productsearch?cate=cgInductors&stype=2&realtime=1&scon=productionStatus;0_avairable@生産中&rows=100"
        page.goto(base_url)

        # 총 데이터 개수 가져오기
        try:
            # 데이터 개수 추출
            total_items_selector = "span.num"  # 수정: 해당 셀렉터를 확인하세요
            page.wait_for_selector(total_items_selector, timeout=10000)  # 10초 대기
            total_items_text = page.locator(total_items_selector).inner_text().strip()
            total_items = int(total_items_text.replace(",", "").strip())  # 쉼표 제거 후 정수 변환
            print(f"총 데이터 개수: {total_items}")

            # 총 페이지 수 계산 (100개씩 표시)
            rows_per_page = 100
            total_pages = math.ceil(total_items / rows_per_page)
            print(f"총 페이지 수: {total_pages}")
        except Exception as e:
            print(f"총 데이터 개수 가져오기 실패: {e}")
            return

        # 모든 페이지 데이터 수집
        all_data = []
        for current_page in range(1, total_pages + 1):
            print(f"{current_page} 페이지 데이터를 가져오는 중...")
            if current_page > 1:
                page.goto(f"{base_url}&pageno={current_page}")
                page.wait_for_selector("table", timeout=60000)  # 테이블 로드 대기

            rows = page.locator("table tbody tr")
            for i in range(rows.count()):
                row_data = rows.nth(i).locator("td").all_inner_texts()
                all_data.append(row_data)

        # 데이터 저장
        column_names = ["Column1", "Column2", "Column3"]  # 실제 열 이름으로 수정
        df = pd.DataFrame(all_data, columns=column_names)
        df.to_excel("murata_data_playwright.xlsx", index=False)
        print("Data saved to murata_data_playwright.xlsx")

        browser.close()

fetch_data()
