from flask import Flask, render_template, request, redirect, url_for
import os
from PyPDF2 import PdfReader
import docx
import spacy
import re

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return redirect(url_for('index'))

    file = request.files['resume']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Check file type and parse accordingly
        if file.filename.endswith('.pdf'):
            parsed_text = parse_pdf(file_path)
        elif file.filename.endswith('.docx'):
            parsed_text = parse_docx(file_path)
        else:
            return "Unsupported file format", 400

        # Clean the parsed text
        parsed_text = parsed_text.replace('\n', ' ').strip()

        # Process the text using spaCy (NLP part)
        doc = nlp(parsed_text)
        parsed_data = extract_info(doc, parsed_text)

        # Save parsed data
        save_parsed_data(parsed_data, file.filename)

        # Render the results page with parsed data
        return render_template('results.html', parsed_data=parsed_data)

def parse_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def parse_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_info(doc, original_text):
    relevant_entities = {}

    # Extract name
    name_pattern = r'(^[A-Z][a-z]+(?:\s[A-Z][a-z]+)*)'
    name_matches = re.findall(name_pattern, original_text)
    relevant_entities['Name'] = name_matches[0] if name_matches else None

    # Extract email and phone number
    relevant_entities['Email'] = extract_email(original_text)
    relevant_entities['Phone'] = extract_phone(original_text)

    # Extract location
    location_pattern = r'\b(?:Austin|San Francisco|New York|Chicago|Los Angeles|Dallas|Texas|California|Florida)\b'
    location_matches = re.findall(location_pattern, original_text)
    relevant_entities['Location'] = location_matches[0] if location_matches else None

    # Capture experience sections with different headers
    experience_section = re.search(r'(?:Relevant Experience|Recent Experience|Experience)(.*?)(?=\n[A-Z]|$)', original_text, re.DOTALL)

    if experience_section:
        print("Extracted Experience Section:", experience_section.group(1).strip())  # Debugging output
        experiences = experience_section.group(1).strip().split('\n\n')  # Split by double newlines for clearer separation

        for exp in experiences:
            # Attempt to capture the position, company, and description
            recent_pattern = r'(?P<position>.*?)\s+at\s+(?P<company>.*?)\s*-\s*(?P<description>.*)'
            match = re.search(recent_pattern, exp)
            if match:
                relevant_entities['Most Recent Experience'] = {
                    'Position': match.group('position').strip(),
                    'Company': match.group('company').strip(),
                    'Description': match.group('description').strip()
                }
                break  # Only get the most recent experience
        else:
            relevant_entities['Most Recent Experience'] = "No relevant experience found."
    else:
        relevant_entities['Most Recent Experience'] = "No experience section found."

    # Extract links (like LinkedIn)
    relevant_entities['Links'] = extract_links(original_text)

    return relevant_entities


def extract_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None

def extract_phone(text):
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    matches = re.findall(phone_pattern, text)
    return matches[0] if matches else None

def extract_links(text):
    link_pattern = r'(https?://[^\s]+)'
    matches = re.findall(link_pattern, text)
    return matches if matches else []

def save_parsed_data(parsed_data, filename):
    output_path = os.path.join('parsed_output', f"{filename}.json")
    with open(output_path, 'w') as f:
        f.write(str(parsed_data))

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('parsed_output'):
        os.makedirs('parsed_output')

    app.run(debug=True)
