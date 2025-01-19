from playwright.sync_api import sync_playwright
import openpyxl
import math

def scrape_and_save_to_excel():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 브라우저 표시
        page = browser.new_page()

        # 첫 페이지 URL
        base_url = "https://www.murata.com/search/productsearch?cate=cgInductors&stype=2&realtime=1&scon=productionStatus;0_avairable@%E7%94%9F%E7%94%A3%E4%B8%AD&rows=100"

        # 첫 페이지로 이동
        page.goto(base_url)
        page.wait_for_load_state("networkidle")

        # 총 건수 확인
        total_items_text = page.locator('app-top-navigation span.num').inner_text()  # span.num에서 총 건수 추출
        total_items = int(total_items_text.replace(",", "").strip())  # 정수로 변환
        total_pages = math.ceil(total_items / 100)  # 한 페이지당 100건 기준으로 페이지 수 계산

        print(f"총 건수: {total_items}, 총 페이지: {total_pages}")

        # 모든 페이지 데이터를 수집
        all_part_numbers = []

        for page_no in range(1, total_pages + 1):
            # 각 페이지 URL 생성
            current_url = f"{base_url}&pageno={page_no}"
            print(f"페이지 {page_no} URL: {current_url}")
            page.goto(current_url)
            page.wait_for_load_state("networkidle")  # JavaScript 로드 완료 대기

            # 현재 페이지 데이터 추출
            raw_data = page.locator("td.col-partnumber a").all_inner_texts()
            part_numbers = [item for item in raw_data if item.strip()]  # 빈 문자열 제거
            all_part_numbers.extend(part_numbers)

        # 브라우저 닫기
        browser.close()

    # 데이터 엑셀로 저장
    save_to_excel(all_part_numbers)
    print("데이터가 성공적으로 Excel 파일로 저장되었습니다!")

def save_to_excel(data):
    # Workbook 생성
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Murata Data"

    # 헤더 추가
    sheet.append(["Part Number"])  # 엑셀 첫 행에 헤더 추가

    # 데이터 추가
    for part_number in data:
        sheet.append([part_number])  # 각 데이터는 한 열에 삽입

    # 엑셀 파일 저장
    workbook.save("Murata_PartNumbers.xlsx")

if __name__ == "__main__":
    scrape_and_save_to_excel()
