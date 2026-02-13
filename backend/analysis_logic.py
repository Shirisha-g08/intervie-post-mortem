import spacy
from textblob import TextBlob
import io
from pypdf import PdfReader
import re

# Load spaCy model (lightweight)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback or download if not present (handled in setup hopefully)
    # In a real scenario we might want to download it here programmatically
    # For now assuming it is installed.
    import en_core_web_sm
    nlp = en_core_web_sm.load()

def extract_text_from_pdf(pdf_bytes):
    """Extracts text from PDF bytes."""
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def extract_keywords(text):
    """Extracts keywords (NOUNs and PROPNs) from text."""
    doc = nlp(text)
    # Filter out stopwords and punctuation
    keywords = [token.lemma_.lower() for token in doc if token.pos_ in ("NOUN", "PROPN") and not token.is_stop and not token.is_punct]
    return set(keywords)

def analyze_match(resume_text, jd_text):
    """Compares resume keywords to JD keywords."""
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)
    
    if not jd_keywords:
        return {
            "match_score": 0,
            "missing_skills": [],
            "explanation": "Job description seems too short or vague."
        }
        
    common_keywords = resume_keywords.intersection(jd_keywords)
    missing_keywords = jd_keywords - resume_keywords
    
    match_score = int((len(common_keywords) / len(jd_keywords)) * 100) if jd_keywords else 0
    
    # Sort missing keywords by frequency in JD? For now just list them.
    # We can assume essential keywords often appear multiple times, but set structure lost that info.
    # Improvement: use Counter for jd_keywords initially to weigh them.
    
    explanation = f"You matched {len(common_keywords)} out of {len(jd_keywords)} derived key terms."
    if match_score < 50:
        explanation += " Your resume seems to miss many critical keywords found in the job description."
    elif match_score < 80:
        explanation += " Good match, but there are some gaps."
    else:
        explanation += " Excellent alignment with the job description."

    return {
        "match_score": match_score,
        "missing_skills": list(missing_keywords)[:10], # Top 10 missing
        "explanation": explanation
    }

def analyze_interview(experience_text):
    """Analyzes interview experience for clarity, confidence, and structure."""
    
    blob = TextBlob(experience_text)
    sentences = blob.sentences
    
    # 1. Clarity & Structure
    # Check for STAR method indicators
    star_keywords = ["situation", "task", "action", "result", "outcome", "challenge", "solved", "achieved"]
    star_matches = [word for word in star_keywords if word in experience_text.lower()]
    
    structure_score = 0
    structure_feedback = []
    
    if len(star_matches) > 3:
        structure_score = 100
        structure_feedback.append("Good use of structured storytelling words.")
    else:
        structure_score = 50
        structure_feedback.append("Your response could be more structured. Try using the STAR method (Situation, Task, Action, Result) explicitly.")
        
    # 2. Confidence Analysis
    # Check for weak words
    weak_words = ["maybe", "sort of", "kind of", "I guess", "I think", "tried to", "basically", "probably"]
    detected_weak_words = [word for word in weak_words if word in experience_text.lower()]
    
    confidence_rating = "High"
    confidence_feedback = []
    
    if len(detected_weak_words) > 0:
        confidence_rating = "Medium" if len(detected_weak_words) < 3 else "Low"
        confidence_feedback.append(f"Avoid hesitate words like: {', '.join(set(detected_weak_words))}.")
        confidence_feedback.append("Use strong action verbs like 'led', 'managed', 'delivered', 'created'.")
    else:
        confidence_feedback.append("Your tone sounds confident and direct.")

    # 3. Clarity (Sentence length and complexity - simple heuristic)
    avg_sentence_length = sum(len(s.words) for s in sentences) / len(sentences) if sentences else 0
    if avg_sentence_length > 25:
        structure_feedback.append("Some sentences are quite long. Try to be more concise.")
    
    return {
        "clarity_score": structure_score, # Mapping structure to clarity for now
        "structure_feedback": structure_feedback,
        "confidence_rating": confidence_rating,
        "confidence_feedback": confidence_feedback,
    }

def generate_feedback(match_analysis, interview_analysis):
    """Combines analyses into final feedback."""
    
    rejection_reasons = []
    
    # Logic for reasons
    if match_analysis["match_score"] < 50:
        rejection_reasons.append({
            "reason": "Skill Mismatch",
            "severity": "High",
            "explanation": "Your resume misses many keywords found in the JD.",
            "fix": " tailored your resume to include the missing skills listed below."
        })
    
    if interview_analysis["confidence_rating"] == "Low":
        rejection_reasons.append({
            "reason": "Low Confidence / Passive Communication",
            "severity": "Medium",
            "explanation": "Your interview answers may have sounded unsure or passive.",
            "fix": "Practice speaking with authority. Own your contributions."
        })
        
    if interview_analysis["clarity_score"] < 70:
        rejection_reasons.append({
            "reason": "Unstructured Answers",
            "severity": "Medium",
            "explanation": "It might have been hard for the interviewer to follow your story.",
            "fix": "Use the STAR method to structure your responses."
        })

    # Fallback if no specific reasons found (i.e. everything looks okayish but still rejected?)
    if not rejection_reasons:
        rejection_reasons.append({
            "reason": "Cultural Fit / Competition",
            "severity": "Low",
            "explanation": "Your metrics look good. It is possible other candidates were just slightly better fits.",
            "fix": "Keep refining your stories and apply to more roles."
        })

    action_plan = {
        "resume_improvements": [f"Add keyword: {kw}" for kw in match_analysis["missing_skills"][:5]],
        "interview_prep": interview_analysis["structure_feedback"] + interview_analysis["confidence_feedback"]
    }

    return {
        "match_score": match_analysis["match_score"],
        "missing_skills": match_analysis["missing_skills"],
        "skill_gap_explanation": match_analysis["explanation"],
        "clarity_score": interview_analysis["clarity_score"],
        "structure_feedback": interview_analysis["structure_feedback"],
        "confidence_rating": interview_analysis["confidence_rating"],
        "confidence_feedback": interview_analysis["confidence_feedback"],
        "rejection_reasons": rejection_reasons,
        "action_plan": action_plan
    }
