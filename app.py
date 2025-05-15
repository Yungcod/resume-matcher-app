import streamlit as st
from utils import get_match_percentage, find_missing_keywords, call_api, create_analysis_prompt

# Page configuration
st.set_page_config(
    page_title="Resume & Job Matcher",
    page_icon=None,
    layout="wide"
)

# CSS styling
st.markdown("""
    <style>
    .stTextArea textarea {
        height: 250px;
        font-size: 16px;
    }
    
    .result-box {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 15px;
        margin: 12px 0;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .warning-box {
        background-color: #FEF3C7;
        border: 1px solid #FCD34D;
        color: #92400E;
        padding: 12px;
        border-radius: 8px;
        margin: 12px 0;
    }
    
    .match-box {
        background-color: #F0F9FF;
        border-radius: 8px;
        padding: 12px;
        margin: 12px 0;
        border: 1px solid #BAE6FD;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("Resume & Job Matcher")

# App description
st.write("""
    This application compares resumes against job descriptions to provide feedback on match quality.
    Enter text in both fields and click the analyze button for results.
""")

# Input columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Job Description")
    job_description = st.text_area(
        "Paste job description",
        placeholder="Enter job description text...",
        key="job_desc"
    )

with col2:
    st.subheader("Resume")
    resume = st.text_area(
        "Paste resume",
        placeholder="Enter resume text...",
        key="resume"
    )

# Center the analyze button
col1, col2, col3 = st.columns([1,2,1])
with col2:
    analyze_button = st.button("Analyze Match", type="primary", use_container_width=True)

# Analysis logic
if analyze_button:
    if not job_description or not resume:
        st.warning("Please fill in both fields.")
    else:
        try:
            with st.spinner("Analyzing..."):
                # Create analysis prompt
                prompt = create_analysis_prompt(job_description, resume)
                
                # Call external API
                result, error = call_api(prompt, st.secrets["API_KEY"])
                
                if error:
                    st.error(f"{error}")
                    st.info("Check API key and connection.")
                else:
                    # Get analysis text
                    feedback_text = result["choices"][0]["message"]["content"]
                    
                    # Extract and show match percentage
                    match_percentage = get_match_percentage(feedback_text)
                    if match_percentage is not None:
                        st.markdown(f"""
                            <div class="match-box">
                                <h3>Match Score</h3>
                                <div style='font-size: 22px; font-weight: bold; color: #3B82F6;'>{match_percentage}%</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.progress(match_percentage / 100)
                    
                    # Show analysis results
                    st.subheader("Analysis Results")
                    st.markdown(f'<div class="result-box">{feedback_text}</div>', unsafe_allow_html=True)
                    
                    # Download option
                    st.download_button(
                        "Download Analysis",
                        feedback_text,
                        file_name="resume_analysis.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    # Show missing keywords
                    missing_keywords = find_missing_keywords(job_description, resume)
                    if missing_keywords:
                        keywords_str = ", ".join(missing_keywords)
                        st.markdown(f"""
                            <div class="warning-box">
                                <strong>Missing Keywords</strong><br>
                                Consider adding these terms: {keywords_str}
                            </div>
                        """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Try again or check your inputs.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6B7280; font-size: 14px;'>
        CS Portfolio Project - 2025
    </div>
""", unsafe_allow_html=True) 