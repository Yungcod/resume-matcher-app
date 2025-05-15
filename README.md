# Resume & Job Matcher

A simple tool to compare your resume against job descriptions using DeepSeek AI.

## About This Project

I created this app as part of my Python programming coursework. It uses AI to analyze resumes against job descriptions to help job seekers improve their applications.

## Features

- Resume and job description comparison
- Match percentage score
- Missing keyword identification
- Resume improvement suggestions
- Clean and intuitive interface

## Project Structure

- `app.py` - Main Streamlit application file
- `utils.py` - Helper functions for API calls and text analysis
- `requirements.txt` - Project dependencies
- `.streamlit/secrets.toml` - Configuration file for API key

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your DeepSeek API key:
   - Create or edit the `.streamlit/secrets.toml` file
   - Add the line `DEEPSEEK_API_KEY = "your-api-key"`

## Running the App

```bash
streamlit run app.py
```

## How to Use

1. Paste a job description in the left field
2. Paste your resume in the right field
3. Click "Analyze Match"
4. Review the analysis and suggestions

## What I Learned

Building this project helped me understand:
- Making API calls with proper error handling
- Using regular expressions for text analysis
- Building user interfaces with Streamlit
- Working with AI language models

## Requirements

- Python 3.7+
- Streamlit
- Requests
- DeepSeek API key

## Note

Keep your API key secure and never share it publicly. 