import re
import requests
from typing import Optional, Dict, Tuple

# API configuration
API_URL = "https://api.textanalysis.service/v1/completions"
SYSTEM_PROMPT = "Analyze resume and job description matching objectively."

def get_match_percentage(text: str) -> Optional[int]:
    """
    Extract percentage match from response text.
    Returns None if no percentage is found.
    """
    patterns = [
        r'(\d+)%',
        r'(\d+)\s*percent',
        r'(\d+)\s*per\s*cent',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return int(match.group(1))
    
    return None

def find_missing_keywords(job_text: str, resume_text: str) -> list:
    """
    Find keywords in job description that are missing from resume.
    Returns up to 10 important keywords.
    """
    job_words = set(re.findall(r'\b\w{4,}\b', job_text.lower()))
    resume_words = set(re.findall(r'\b\w{4,}\b', resume_text.lower()))
    
    common_words = {'work', 'team', 'project', 'experience', 'skills', 'ability'}
    missing = job_words - resume_words - common_words
    
    return sorted(list(missing))[:10]

def call_api(prompt: str, api_key: str) -> Tuple[Dict, Optional[str]]:
    """
    Send request to text analysis API and get response.
    Returns (response_json, None) if successful or (None, error_message) if failed.
    """
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "language-model",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json(), None
        
    except requests.exceptions.RequestException as e:
        return None, f"API Error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def create_analysis_prompt(job_description: str, resume: str) -> str:
    """
    Create prompt for resume/job description comparison.
    """
    return f"""Compare this resume and job description. Analyze:
    1. How well does the resume match (in percentage and words)
    2. What key terms from the job description are missing in the resume
    3. What 3-5 phrases should be replaced in the resume
    4. 1-2 tips for improvement (style, structure, presentation)

    Job Description:
    {job_description}

    Resume:
    {resume}""" 