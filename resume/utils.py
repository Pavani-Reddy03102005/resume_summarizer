import PyPDF2
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def generate_summary(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return " ".join(sentences[:3])


def extract_skills(text):
    SKILLS = ["Python", "Django", "SQL", "Machine Learning", "HTML", "CSS"]

    return [skill for skill in SKILLS if skill.lower() in text.lower()]


def generate_match_score(text):
    score = 0

    if "python" in text.lower():
        score += 30
    if "django" in text.lower():
        score += 20
    if "sql" in text.lower():
        score += 20

    return min(score, 100)