import spacy
import fitz  # PyMuPDF
import docx
import re

# Load your custom address model
nlp = spacy.load("model/data_model")

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text() + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
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

def main():
    # Set the file path here
    file_path = "/Users/jonathanboyd/Documents/Website/Resume.pdf"  # Change this to your PDF or DOCX file path

    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        print("Invalid file type. Please provide a PDF or DOCX file.")
        return

    # Print the processed text
    print("Processed Text:")
    print(text)

    info = extract_information(text)

    print("Extracted Information:")
    print(f"First Name: {info['first_name']}")
    print(f"Last Name: {info['last_name']}")
    print(f"Address: {info['address']}")
    print(f"Phone Number: {info['phone_number']}")
    print(f"Email: {info['email']}")

if __name__ == "__main__":
    main()