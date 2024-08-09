from flask import Flask, request, render_template
from parse import extract_keywords, match_keywords, extract_text_from_pdf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    resume_file = request.files['resume']
    if resume_file.filename.endswith('.pdf'):
        resume_text = extract_text_from_pdf(resume_file)
    else:
        return "Please upload a PDF file."

    job_description = request.form['job_description']
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)
    
    score = match_keywords(resume_keywords, job_keywords)
    total_keywords = len(job_keywords)
    percentage_match = round((score / total_keywords) * 100, 2) if total_keywords > 0 else 0.00

    matched_keywords = sorted(resume_keywords.intersection(job_keywords))
    unmatched_keywords = sorted(job_keywords.difference(matched_keywords))
    
    suggestions = generate_suggestions(unmatched_keywords)

    return render_template('results.html', 
                           score=score, 
                           percentage_match=percentage_match, 
                           matched_keywords=matched_keywords, 
                           suggestions=suggestions)

def generate_suggestions(unmatched_keywords):
    suggestions = []
    if unmatched_keywords:
        suggestions.append(f"Consider including the following keywords in your resume to better match the job description: {', '.join(unmatched_keywords)}")
    else:
        suggestions.append("Your resume is well-aligned with the job description.")
    return suggestions

if __name__ == '__main__':
    app.run(debug=True)
