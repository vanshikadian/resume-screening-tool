import spacy
import pdfplumber
# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# List of filler words to exclude
filler_words = set([
    'the', 'and', 'to', 'of', 'a', 'in', 'for', 'on', 'with', 'as', 
    'by', 'at', 'from', 'is', 'that', 'an', 'be', 'this', 'which', 
    'or', 'it', 'are', 'was', 'can', 'has', 'have', 'had'
])

def extract_keywords(resume_text):
    """
    Extracts unique, meaningful keywords from the resume text using spaCy NLP model.
    It focuses on extracting nouns, proper nouns, and verbs, excluding filler words.
    
    Args:
    - resume_text (str): The text content of the resume.
    
    Returns:
    - set: A set of unique, filtered keywords in lowercase.
    """
    doc = nlp(resume_text)
    keywords = set()
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN', 'VERB'] and token.lemma_.lower() not in filler_words:
            keywords.add(token.lemma_.lower())
    return keywords


def match_keywords(resume_keywords, job_description_keywords):
    """
    Matches the extracted resume keywords with the job description keywords.
    Calculates a matching score based on the number of common keywords.
    
    Args:
    - resume_keywords (list): List of keywords extracted from the resume.
    - job_description_keywords (list): List of keywords extracted from the job description.
    
    Returns:
    - int: A matching score representing the number of matched keywords.
    """
    match_count = sum(1 for keyword in resume_keywords if keyword in job_description_keywords)
    return match_count

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file using pdfplumber.
    
    Args:
    - pdf_file: A file-like object representing the PDF.
    
    Returns:
    - str: Extracted text from the PDF.
    """
    with pdfplumber.open(pdf_file) as pdf:
        pages = [page.extract_text() for page in pdf.pages]
    return "\n".join(pages)
