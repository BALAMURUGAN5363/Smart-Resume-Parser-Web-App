import os
import mimetypes
import pdfplumber
import json
import re
from PIL import Image
import pytesseract  # To extract text from images

def clean_text(text):
    return " ".join(text.split()) if text else None

def decode_unicode_escape_sequences(text):
    escape_sequence_pattern = r'\\u[0-9A-Fa-f]{4}|\\U[0-9A-Fa-f]{8}|\\[0-7]{1,3}|\\x[0-9A-Fa-f]{2}'
    def replace_match(match):
        escape_sequence = match.group(0)
        return bytes(escape_sequence, "utf-8").decode("unicode_escape")
    return re.sub(escape_sequence_pattern, replace_match, text)

def extract_and_map_table(page):
    tables = page.extract_tables()
    mapped_tables = []
    for table in tables:
        if table and len(table) > 1:
            headers = [clean_text(cell) for cell in table[0]]
            for row in table[1:]:
                mapped_row = {headers[i]: clean_text(cell) for i, cell in enumerate(row) if i < len(headers)}
                mapped_tables.append(mapped_row)
    return mapped_tables

def extract_images_from_pdf(file, output_dir="extracted_images"):
    os.makedirs(output_dir, exist_ok=True)
    image_paths = []
    with pdfplumber.open(file) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for i, img_obj in enumerate(page.images):
                x0, top, x1, bottom = img_obj["x0"], img_obj["top"], img_obj["x1"], img_obj["bottom"]
                cropped_image = page.crop((x0, top, x1, bottom)).to_image()
                output_file = os.path.join(output_dir, f"page_{page_number}_image_{i + 1}.png")
                cropped_image.save(output_file)
                image_paths.append(output_file)
    return image_paths

def extract_text_from_images(image_paths):
    ocr_text = []
    for image_path in image_paths:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        ocr_text.append(text)
    return "\n".join(ocr_text)

def process_pdf(file):
    pdf_data = {"file_type": "PDF", "pages": []}
    plain_text_pages = []

    # Extract images
    images = extract_images_from_pdf(file)

    # Extract text from images (OCR)
    pdf_images_text = extract_text_from_images(images)

    file.seek(0)  # Reset file pointer after reading images
    with pdfplumber.open(file) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_data = {"page_number": page_number, "text": None, "tables": []}
            text = page.extract_text()
            if text:
                cleaned_text = clean_text(text)
                decoded_text = decode_unicode_escape_sequences(cleaned_text)
                page_data["text"] = decoded_text
                plain_text_pages.append(f"Page {page_number}:\n{decoded_text}\n")
            tables = extract_and_map_table(page)
            if tables:
                page_data["tables"].extend(tables)
            pdf_data["pages"].append(page_data)

    pdf_data["txt_content"] = "\n".join(plain_text_pages)
    pdf_data["images"] = images

    # Return structured data, plain text, and OCR text (from images)
    return pdf_data, "\n".join(plain_text_pages), pdf_images_text

def process_txt(file):
    text = file.read().decode("utf-8")
    cleaned_text = clean_text(text)
    decoded_text = decode_unicode_escape_sequences(cleaned_text)
    return {"file_type": "TXT", "content": decoded_text, "txt_content": decoded_text}

def process_file(file_storage):
    filename = file_storage.filename
    mime_type, _ = mimetypes.guess_type(filename)

    if mime_type == "application/pdf":
        return process_pdf(file_storage)
    elif mime_type == "text/plain":
        return process_txt(file_storage), []
    else:
        return {"error": f"Unsupported file type: {mime_type}"}, []
"""
import pdfplumber
import pytesseract
from PIL import Image
import os

def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_images_from_pdf(filepath, output_folder="extracted_images"):
    os.makedirs(output_folder, exist_ok=True)
    image_paths = []
    with pdfplumber.open(filepath) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for img_index, img_obj in enumerate(page.images):
                x0, top, x1, bottom = img_obj["x0"], img_obj["top"], img_obj["x1"], img_obj["bottom"]
                cropped_image = page.crop((x0, top, x1, bottom)).to_image()
                image_path = os.path.join(output_folder, f"page_{page_number}_img_{img_index}.png")
                cropped_image.save(image_path)
                image_paths.append(image_path)
    return image_paths

def ocr_text_from_images(image_paths):
    text = ""
    for img_path in image_paths:
        img = Image.open(img_path)
        text += pytesseract.image_to_string(img) + "\n"
    return text.strip()

import pytesseract  # To extract text from images
import os
import mimetypes
import pdfplumber
import json
import re
from PIL import Image
import pytesseract

def clean_text(text):
    return " ".join(text.split()) if text else None

def decode_unicode_escape_sequences(text):
    escape_sequence_pattern = r'\\u[0-9A-Fa-f]{4}|\\U[0-9A-Fa-f]{8}|\\[0-7]{1,3}|\\x[0-9A-Fa-f]{2}'
    def replace_match(match):
        escape_sequence = match.group(0)
        return bytes(escape_sequence, "utf-8").decode("unicode_escape")
    return re.sub(escape_sequence_pattern, replace_match, text)

def extract_and_map_table(page):
    tables = page.extract_tables()
    mapped_tables = []
    for table in tables:
        if table and len(table) > 1:
            headers = [clean_text(cell) for cell in table[0]]
            for row in table[1:]:
                mapped_row = {headers[i]: clean_text(cell) for i, cell in enumerate(row) if i < len(headers)}
                mapped_tables.append(mapped_row)
    return mapped_tables

def extract_images_from_pdf(file_path, output_dir="extracted_images"):
    os.makedirs(output_dir, exist_ok=True)
    image_paths = []
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for i, img_obj in enumerate(page.images):
                x0, top, x1, bottom = img_obj["x0"], img_obj["top"], img_obj["x1"], img_obj["bottom"]
                cropped_image = page.crop((x0, top, x1, bottom)).to_image()
                output_file = os.path.join(output_dir, f"page_{page_number}_image_{i + 1}.png")
                cropped_image.save(output_file)
                image_paths.append(output_file)
    return image_paths

def extract_text_from_images(image_paths):
    ocr_text = []
    for image_path in image_paths:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        ocr_text.append(text)
    return "\n".join(ocr_text)

def process_pdf(file_path):
    pdf_data = {"file_type": "PDF", "pages": []}
    plain_text_pages = []
    image_paths = extract_images_from_pdf(file_path)
    ocr_text = extract_text_from_images(image_paths)

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_data = {"page_number": page_number, "text": None, "tables": []}
            text = page.extract_text()
            if text:
                cleaned_text = clean_text(text)
                decoded_text = decode_unicode_escape_sequences(cleaned_text)
                page_data["text"] = decoded_text
                plain_text_pages.append(f"Page {page_number}:\n{decoded_text}\n")

            tables = extract_and_map_table(page)
            if tables:
                page_data["tables"].extend(tables)

            pdf_data["pages"].append(page_data)

    pdf_data["txt_content"] = "\n".join(plain_text_pages)
    pdf_data["ocr_text"] = ocr_text
    pdf_data["images"] = image_paths
    return pdf_data, plain_text_pages
# main() removed — process_pdf will now be called from app.py

import os
import mimetypes
import pdfplumber
import re


def clean_text(text):
    return " ".join(text.split()) if text else None


def decode_unicode_escape_sequences(text):
    escape_sequence_pattern = r'\\u[0-9A-Fa-f]{4}|\\U[0-9A-Fa-f]{8}|\\[0-7]{1,3}|\\x[0-9A-Fa-f]{2}'

    def replace_match(match):
        escape_sequence = match.group(0)
        try:
            return bytes(escape_sequence, "utf-8").decode("unicode_escape")
        except:
            return escape_sequence  # Return as-is if decoding fails

    return re.sub(escape_sequence_pattern, replace_match, text)


def extract_and_map_table(page):
    tables = page.extract_tables()
    mapped_tables = []

    for table in tables:
        if table and len(table) > 1:  # Ensure the table has headers and rows
            headers = [clean_text(cell) for cell in table[0]]
            for row in table[1:]:
                mapped_row = {headers[i]: clean_text(cell) for i, cell in enumerate(row) if i < len(headers)}
                mapped_tables.append(mapped_row)

    return mapped_tables


def extract_images_from_pdf(file_path, output_dir="extracted_images"):
    os.makedirs(output_dir, exist_ok=True)
    image_paths = []

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for i, img_obj in enumerate(page.images):
                x0, top, x1, bottom = img_obj["x0"], img_obj["top"], img_obj["x1"], img_obj["bottom"]
                cropped_image = page.crop((x0, top, x1, bottom)).to_image()
                output_file = os.path.join(output_dir, f"page_{page_number}_image_{i + 1}.png")
                cropped_image.save(output_file)
                image_paths.append(output_file)

    return image_paths


def process_pdf(file_path):
    pdf_data = {"file_type": "PDF", "pages": []}
    plain_text_pages = []
    images = extract_images_from_pdf(file_path)

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_data = {"page_number": page_number, "text": None, "tables": []}
            text = page.extract_text()

            if text:
                cleaned_text = clean_text(text)
                decoded_text = decode_unicode_escape_sequences(cleaned_text)
                page_data["text"] = decoded_text
                plain_text_pages.append(f"Page {page_number}:\n{decoded_text}\n")

            tables = extract_and_map_table(page)
            if tables:
                page_data["tables"].extend(tables)

            pdf_data["pages"].append(page_data)

    pdf_data["txt_content"] = "\n".join(plain_text_pages)
    pdf_data["images"] = images
    return pdf_data, plain_text_pages


def process_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as txt_file:
        text = txt_file.read()
    cleaned_text = clean_text(text)
    decoded_text = decode_unicode_escape_sequences(cleaned_text)
    return {
        "file_type": "TXT",
        "content": decoded_text,
        "txt_content": decoded_text
    }


def process_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type == "application/pdf":
        return process_pdf(file_path)
    elif mime_type == "text/plain":
        return process_txt(file_path), []
    else:
        return {"error": f"Unsupported file type: {mime_type}"}, []
"""