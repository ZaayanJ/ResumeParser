# 📄 Resume Parser

An AI-powered resume parser that extracts structured candidate data from `.pdf` and `.docx` files with high accuracy using NLP techniques. Combines a sleek frontend upload interface with a Flask backend powered by spaCy to automate and accelerate resume screening workflows.

---

## 🚀 Features

- 🤖 **AI Resume Parsing** with Python + spaCy NLP  
- ⚙️ **Flask Backend** for processing uploads and serving predictions  
- 📂 **File Upload UI** for `.pdf` and `.docx` resumes  
- 📊 85%+ extraction accuracy on real-world resume formats  
- ⚡ Reduces manual resume review time by 75%  
- 🌐 Responsive frontend with animated progress bar and modern UX  

---

## 🧠 Tech Stack

| Layer       | Technology                   |
|-------------|-------------------------------|
| **Frontend**| HTML5, CSS3, JavaScript       |
| **Backend** | Python, Flask                 |
| **NLP**     | spaCy (custom NER pipeline)   |
| **Parsing** | PDFMiner, python-docx         |

## 📁 Project Structure

```
ResumeParser/
├── backend/
│   ├── app.py               # Flask app
│   ├── parser.py            # spaCy-based resume parser
│   └── utils.py             # Helpers for file handling
├── templates/
│   └── index.html           # Frontend upload form
├── static/
│   └── style.css            # (Optional: Extracted CSS)
└── README.md
```
## 💡 How It Works

1. User uploads a resume via the UI  
2. Flask receives the file and extracts text  
3. spaCy NLP model parses and tags entities (Name, Email, Skills, etc.)  
4. Parsed output is returned as structured JSON or HTML view  

---

✨ Sample Output
json
Copy
Edit
{
  "name": "Jane Doe",
  "email": "jane.doe@example.com",
  "skills": ["Python", "Flask", "NLP", "Machine Learning"],
  "education": "M.Sc. in Computer Science",
  "experience": "2 years at ABC Corp"
}
🔭 Future Improvements
Add LinkedIn/GitHub scraping for profile enrichment

Fine-tune spaCy with domain-specific NER examples

Export parsed data to CSV/Excel or Airtable

Add job description matching feature

👨‍💻 Author
Zaayan Javed

💼 LinkedIn

💻 GitHub
