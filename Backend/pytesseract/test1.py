from PIL import Image
import pytesseract
import cv2
import json
image = input("Enter the image path:").strip().strip('"')
file = Image.open(image)
try:
    img = cv2.imread(image)
    gray =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    temp_path = "temp_processed_image.png"
    cv2.imwrite(temp_path, gray)
    text = pytesseract.image_to_string(temp_path).replace("\t"," ").strip()
    text_lines = text.split("\n")
    text_lines = [line.strip() for line in text_lines if line.strip()]
    json_output = {"Extracted Text": text_lines}
    print("\nJSON Output:")
    print(json.dumps(json_output, indent=4, ensure_ascii=False))
    json_file = "extracted_text.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4, ensure_ascii=False)
    print("Extracted text:")
    print(text)
    print(f" JSON saved in: {json_file}")
    text_file = "extracted_text.txt"
    with open(text_file, "w", encoding="utf-8") as f:
        f.write("\n".join(text_lines))
except FileNotFoundError:
    print("Error: File not found. Please check the path and try again.")

