import re
import requests
from typing import Optional, Dict, Tuple

# My custom configuration for DeepSeek API
# I found this endpoint in their documentation
API_URL = "https://api.deepseek.com/v1/chat/completions"
# I tried different prompts, this one works best!
SYSTEM_PROMPT = "You are a professional resume and job matching expert."

def get_match_percentage(text: str) -> Optional[int]:
    """
    Extract percentage match from AI response text.
    Returns None if no percentage is found.
    
    This was tricky to implement because AI responses vary a lot!
    """
    # Looking for percentage patterns like '75%', '75 percent', etc.
    patterns = [
        r'(\d+)%',
        r'(\d+)\s*percent',
        r'(\d+)\s*per\s*cent',
    ]
    
    # Check each pattern
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            # Return the percentage as an integer
            return int(match.group(1))
    
    # If no percentage found
    return None

def find_missing_keywords(job_text: str, resume_text: str) -> list:
    """
    Find keywords that are in job description but missing from resume.
    Returns a list of up to 10 important missing keywords.
    
    I made this to help identify key skills that might be missing!
    """
    # Find all words with 4+ characters in both texts
    job_words = set(re.findall(r'\b\w{4,}\b', job_text.lower()))
    resume_words = set(re.findall(r'\b\w{4,}\b', resume_text.lower()))
    
    # Ignore common words that appear in almost every resume/job description
    # I manually created this list based on my analysis of job postings
    common_words = {'work', 'team', 'project', 'experience', 'skills', 'ability'}
    
    # Find words that exist in job description but not in resume
    missing = job_words - resume_words - common_words
    
    # Return up to 10 words
    return sorted(list(missing))[:10]

def call_ai_api(prompt: str, api_key: str) -> Tuple[Dict, Optional[str]]:
    """
    Send request to DeepSeek API and get response.
    Returns (response_json, None) if successful or (None, error_message) if failed.
    
    This took me a while to get right with proper error handling!
    """
    try:
        # Headers for API request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Data to send
        data = {
            "model": "deepseek-chat",  # Found this was the best model for this task
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,  # Controls creativity of response
            "max_tokens": 1000   # Maximum response length
        }

        # Send POST request to API
        response = requests.post(API_URL, headers=headers, json=data)
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # Return parsed JSON response
        return response.json(), None
        
    except requests.exceptions.RequestException as e:
        # API and network related errors
        return None, f"API Error: {str(e)}"
    except Exception as e:
        # Other errors
        return None, f"Unexpected error: {str(e)}"

def create_analysis_prompt(job_description: str, resume: str) -> str:
    """
    Create prompt for the AI to analyze resume against job description.
    
    I experimented with different prompt structures and this gave the best results!
    """
    # My custom prompt template - spent time refining this!
    return f"""Compare this resume and job description. Analyze:
    1. How well does the resume match (in percentage and words)
    2. What key terms from the job description are missing in the resume
    3. What 3-5 phrases should be replaced in the resume
    4. 1-2 tips for improvement (style, structure, presentation)

    Job Description:
    {job_description}

    Resume:
    {resume}""" 