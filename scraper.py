from playwright.sync_api import sync_playwright
import os

def scrape_links():
    # 결과 저장 폴더 생성
    os.makedirs("results", exist_ok=True)

    with sync_playwright() as p:
        # Playwright로 Chromium 브라우저 실행
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 네이버 메인 페이지 열기
        url = "https://news.naver.com/"
        page.goto(url)

        # <title> 태그의 텍스트 가져오기
        title_text = page.title()  # Playwright의 title() 메서드 사용
        print(f"페이지 제목: {title_text}")

        # 결과 저장
        with open("results/title.txt", "w", encoding="utf-8") as f:
            f.write(title_text)
            
        print("텍스트 추출 완료! -> results/extracted_text.txt")


        # 특정 요소가 나타날 때까지 대기
        page.wait_for_selector("a[href]")
        # 2. 링크 추출
        links = page.query_selector_all("a[href]")  # 모든 'a' 태그의 'href' 속성 가져오기
        with open("results/links.txt", "w", encoding="utf-8") as f:
            for link in links:
                href = link.get_attribute("href")
                if href and (".pdf" in href or ".jpg" in href or ".png" in href):
                    f.write(href + "\n")
        print("링크 추출 완료! -> results/links.txt")

        # 브라우저 종료
        browser.close()

if __name__ == "__main__":
    scrape_links()