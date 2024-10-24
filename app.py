from flask import Flask, request, render_template, jsonify  # Added render_template back to the import
from flask_cors import CORS  # Import CORS
import spacy
import pdfplumber
import docx
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
nlp = spacy.load("model/data_model")  # Load your custom address model

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_information(text):
    doc = nlp(text)
    first_name = ""
    last_name = ""
    address = ""
    phone_number = ""
    email = ""

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            names = ent.text.split()
            if len(names) >= 2:
                first_name, last_name = names[0], names[1]
        elif ent.label_ == "GPE":
            address = ent.text
        elif ent.label_ == "PHONE":
            phone_number = ent.text
        elif ent.label_ == "EMAIL":
            email = ent.text

    # Regex for phone number and email
    phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    phone_match = phone_pattern.findall(text)
    email_match = email_pattern.findall(text)

    if phone_match:
        phone_number = phone_match[0]
    if email_match:
        email = email_match[0]

    return {
        "first_name": first_name,
        "last_name": last_name,
        "address": address,
        "phone_number": phone_number,
        "email": email,
    }

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file and (file.filename.endswith('.pdf') or file.filename.endswith('.docx')):
            if file.filename.endswith('.pdf'):
                text = extract_text_from_pdf(file)
            else:
                text = extract_text_from_docx(file)

            info = extract_information(text)
            return jsonify(info)  # Return JSON response instead of rendering a template

    return render_template("upload.html")  # Render upload page on GET requests

if __name__ == "__main__":
    app.run(debug=True)