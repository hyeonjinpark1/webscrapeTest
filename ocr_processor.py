import os
from PIL import Image
import pytesseract

# Tesseract 실행 파일 경로 설정 (Windows 사용자용)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_images(folder_path, output_file):
    """
    주어진 폴더의 모든 이미지에서 텍스트를 추출하고 결과를 저장합니다.
    """
    # 이미지 파일 목록 가져오기
    image_files = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.lower().endswith((".jpg", ".png", ".jpeg"))
    ]

    if not image_files:
        print("이미지 파일이 존재하지 않습니다.")
        return

    results = []

    for image_file in image_files:
        try:
            # 이미지 열기 및 OCR 수행
            image = Image.open(image_file)
            text = pytesseract.image_to_string(image, lang="kor+eng")  # 필요한 언어 설정
            print(f"OCR 완료: {image_file}")
            results.append({"file_name": image_file, "text": text.strip()})
        except Exception as e:
            print(f"OCR 실패: {image_file}, 에러: {e}")
            results.append({"file_name": image_file, "text": None})

    # 결과를 텍스트 파일에 저장
    with open(output_file, "w", encoding="utf-8") as f:
        for result in results:
            f.write(f"파일: {result['file_name']}\n")
            f.write(f"텍스트:\n{result['text']}\n")
            f.write("-" * 40 + "\n")

    print(f"OCR 처리 완료! 결과 저장 -> {output_file}")

if __name__ == "__main__":
    # 이미지 파일이 저장된 폴더 경로
    folder_path = "downloads/images"
    # OCR 결과 저장 파일
    output_file = "results/image_texts.txt"

    extract_text_from_images(folder_path, output_file)
