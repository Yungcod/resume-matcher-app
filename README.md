# Resume & Job Matcher

A tool to compare resumes against job descriptions using text analysis.

## Project Overview

This application was developed as part of a programming course project. It analyzes resumes against job descriptions to provide matching feedback.

## Screenshot 
![image](https://github.com/user-attachments/assets/5d5bda3b-9c43-4a35-902e-1cf6171d6cdf)





## Features

- Resume and job description comparison
- Match percentage calculation
- Keyword analysis
- Improvement suggestions
- Simple user interface

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
3. Set up your API key:
   - Create or edit the `.streamlit/secrets.toml` file
   - Add the line `DEEPSEEK_API_KEY = "your-api-key"`

## Running the Application

```bash
streamlit run app.py
```

## Usage Instructions

1. Enter job description in the left field
2. Enter resume in the right field
3. Click "Analyze Match"
4. Review the analysis and suggestions

## Requirements

- Python 3.7+
- Streamlit
- Requests
- API key (external text analysis service)

## Notes

- This is a course project and may have limitations
- Keep your API key secure 
