import streamlit as st
import json
from utils import get_match_percentage, find_missing_keywords, call_ai_api, create_analysis_prompt

# Page setup - I tried different layouts and this one looks best
st.set_page_config(
    page_title="Resume & Job Matcher",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS - I learned some CSS tricks for this project!
st.markdown("""
    <style>
    /* Main text area styling */
    .stTextArea textarea {
        height: 250px;
        font-size: 16px;
    }
    
    /* Results container - added shadow for depth */
    .result-box {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Warning box - yellow is good for caution */
    .warning-box {
        background-color: #FEF3C7;
        border: 1px solid #FCD34D;
        color: #92400E;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    /* Match score box - blue feels professional */
    .match-box {
        background-color: #F0F9FF;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        border: 1px solid #BAE6FD;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("🎯 Resume & Job Matcher")

# App description
st.write("""
    This app analyzes how well your resume matches a job description using AI.
    Just paste both texts and click the analyze button to get detailed feedback!
""")

# Create two columns for inputs
col1, col2 = st.columns(2)

# Job description column
with col1:
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        "Paste job description here",
        placeholder="Enter the full job description...",
        key="job_desc"
    )

# Resume column  
with col2:
    st.subheader("📄 Your Resume")
    resume = st.text_area(
        "Paste resume here",
        placeholder="Enter your resume text...",
        key="resume"
    )

# Center the analyze button for better UI
col1, col2, col3 = st.columns([1,2,1])
with col2:
    # I made this button wider to make it more prominent
    analyze_button = st.button("🔍 Analyze Match", type="primary", use_container_width=True)

# Main analysis logic
if analyze_button:
    # Validate inputs first
    if not job_description or not resume:
        st.warning("⚠️ Please fill in both the job description and resume fields.")
    else:
        try:
            # Show loading indicator while processing
            with st.spinner("🤖 Analyzing your resume..."):
                
                # Create prompt for AI analysis
                prompt = create_analysis_prompt(job_description, resume)
                
                # Call DeepSeek API - my custom function from utils.py!
                result, error = call_ai_api(prompt, st.secrets["DEEPSEEK_API_KEY"])
                
                # Check for errors
                if error:
                    st.error(f"❌ {error}")
                    st.info("Please check your API key and internet connection.")
                else:
                    # Extract feedback text from API response
                    feedback_text = result["choices"][0]["message"]["content"]
                    
                    # Try to extract match percentage - this was challenging!
                    match_percentage = get_match_percentage(feedback_text)
                    
                    # Display match percentage if found
                    if match_percentage is not None:
                        st.markdown(f"""
                            <div class="match-box">
                                <h3>Resume Match Score</h3>
                                <div style='font-size: 24px; font-weight: bold; color: #3B82F6;'>{match_percentage}%</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Add progress bar for visual representation
                        st.progress(match_percentage / 100)
                    
                    # Display main AI feedback
                    st.subheader("💡 AI Analysis")
                    st.markdown(f'<div class="result-box">{feedback_text}</div>', unsafe_allow_html=True)
                    
                    # Add download button - neat feature I added!
                    st.download_button(
                        "📥 Download Analysis",
                        feedback_text,
                        file_name="resume_analysis.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    # Find missing keywords - my favorite feature I built
                    missing_keywords = find_missing_keywords(job_description, resume)
                    
                    # Display missing keywords if any found
                    if missing_keywords:
                        keywords_str = ", ".join(missing_keywords)
                        st.markdown(f"""
                            <div class="warning-box">
                                <strong>⚠️ Potential Missing Keywords</strong><br>
                                Consider adding these terms to your resume: {keywords_str}
                            </div>
                        """, unsafe_allow_html=True)

        # Handle any unexpected errors
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
            st.info("Please try again or contact the developer for help.")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #6B7280; font-size: 14px;'>
        Made with ❤️ using Streamlit and DeepSeek AI<br>
        <small>Student Project 2024 - John Doe</small>
    </div>
""", unsafe_allow_html=True) 