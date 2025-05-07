import pytesseract
import cv2
import tempfile
import os
from PIL import Image
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\aarthysasi\Tesseract-OCR\tesseract.exe"
def process_image(file_storage):
    """
    Process an uploaded image file using pytesseract with preprocessing,
    and return extracted text as JSON.
    
    :param file_storage: In-memory file from Flask (request.files['file'])
    :return: (json_result, plain_text)
    """
    
    try:
        # Convert to OpenCV format (np.array)
        image = Image.open(file_storage).convert("RGB")
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Resize while keeping aspect ratio
        width = 800
        height = int((width / img_cv.shape[1]) * img_cv.shape[0])
        resized_img = cv2.resize(img_cv, (width, height))

        # Preprocess: Grayscale, Thresholding, Dilation
        gray = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        _, binary_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated = cv2.dilate(binary_inv, kernel, iterations=1)

        # Save to temporary file for pytesseract
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_path = temp_file.name
            cv2.imwrite(temp_path, dilated)

        # OCR
        custom_config = r'--psm 6'
        text = pytesseract.image_to_string(temp_path, config=custom_config).replace("\t", " ").strip()

        # Cleanup
        os.remove(temp_path)

        text_lines = [line.strip() for line in text.split("\n") if line.strip()]
        json_output = {"Extracted Text": text_lines}
        plain_text = "\n".join(text_lines)

        return json_output, plain_text

    except Exception as e:
        return {"error": str(e)}, ""
print("hi")