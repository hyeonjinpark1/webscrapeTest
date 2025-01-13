import os
import requests

def download_images(link_file, download_folder):
    os.makedirs(download_folder, exist_ok=True)  # 다운로드 폴더 생성

    with open(link_file, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f.readlines()]

    for idx, link in enumerate(links, start=1):
        try:
            # 파일명 생성
            file_name = os.path.join(download_folder, f"image_{idx}.jpg")
            
            # 이미지 다운로드
            print(f"다운로드 중: {link}")
            response = requests.get(link, stream=True)
            response.raise_for_status()  # 요청 실패 시 에러 발생
            
            # 이미지 저장
            with open(file_name, "wb") as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            print(f"다운로드 완료: {file_name}")
        except Exception as e:
            print(f"다운로드 실패: {link}, 에러: {e}")

if __name__ == "__main__":
    # 이미지 링크 파일 경로와 다운로드 폴더 설정
    link_file = "results/image_links.txt"
    download_folder = "downloads/images"

    download_images(link_file, download_folder)
