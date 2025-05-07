from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.extract_pdf import process_pdf
from utils.extract_image import process_image
from utils.spacy_process import run_spacy
from utils.compare_json import compare_jsons
import os

app = Flask(__name__)
CORS(app)  # Allow CORS for frontend like Angular

@app.route('/extract', methods=['POST'])
def extract_file():
    file = request.files.get('file')
    file_path = request.form.get('file_path') or (request.json.get('file_path') if request.is_json else None)

    if not file and not file_path:
        return jsonify({"error": "No file or file path provided"}), 400

    raw_text = ""
    extracted_json = {}

    try:
        if file:
            filename = file.filename.lower()
            file_to_process = file
        elif file_path:
            if not os.path.exists(file_path):
                return jsonify({"error": f"File not found at path: {file_path}"}), 404
            filename = os.path.basename(file_path).lower()
            file_to_process = open(file_path, 'rb')
        else:
            return jsonify({"error": "Invalid input"}), 400

        if filename.endswith('.pdf'):
            extracted_json, pdf_text, pdf_images_text = process_pdf(file_to_process)
            raw_text = pdf_text + "\n" + pdf_images_text
        else:
            extracted_json, raw_text = process_image(file_to_process)

        if file_path:
            file_to_process.close()

        spacy_json = run_spacy(raw_text)
        final_json = compare_jsons([extracted_json, spacy_json])

        return jsonify({
            "final_json": final_json,
            "raw_text": raw_text,
            "spacy_json": spacy_json
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
"""from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.extract_pdf import process_pdf
from utils.extract_image import process_image
from utils.spacy_process import run_spacy
from utils.compare_json import compare_jsons
import os

app = Flask(__name__)
CORS(app)  # Allow CORS

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/extract', methods=['POST'])
def extract_file():
    try:
        # Get the uploaded file
        file = request.files.get('file')

        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Save the uploaded file temporarily
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        raw_text = ""
        extracted_json = {}

        if filename.lower().endswith('.pdf'):
            with open(filepath, 'rb') as f:
                extracted_json, pdf_text, pdf_images_text = process_pdf(f)
                raw_text = (pdf_text or "") + "\n" + (pdf_images_text or "")
        else:
            with open(filepath, 'rb') as f:
                extracted_json, raw_text = process_image(f)

        # Now run spaCy on the extracted text
        spacy_json = run_spacy(raw_text or "")

        # Compare JSONs to choose best
        final_json = compare_jsons([extracted_json, spacy_json])

        # Clean up
        os.remove(filepath)

        return jsonify({
            "final_json": final_json,
            "raw_text": raw_text,
            "spacy_json": spacy_json
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.extract_pdf import process_pdf
from utils.extract_image import process_image
from utils.spacy_process import run_spacy

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        if filename.lower().endswith('.pdf'):
            pdf_data, _ = process_pdf(filepath)
            return jsonify({"result": pdf_data})


        elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            extracted_json, raw_text = process_image(filepath)
            if not isinstance(raw_text, str):
                raise ValueError(f"Expected string for raw_text, got {type(raw_text)} instead")
            spacy_json = run_spacy(raw_text)
            return jsonify({"result": spacy_json})

        else:
            return jsonify({"error": "Unsupported file type."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)"""