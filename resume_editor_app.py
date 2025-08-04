import streamlit as st

from resume_editor_llm import rewrite_resume_snippet

st.set_page_config(layout="centered", page_title="AI Resume Editor")

st.title("AI Resume Editor")
st.markdown("---")

st.write(
    "Paste your resume snippet below, and our AI will rewrite it to be more professional, clear, and impactful."
)

original_snippet = st.text_area(
    "Paste your resume snippet here:",
    height=150,
    placeholder="e.g., 'Managed team. Did sales. Helped customers.'"
)

if st.button("Rewrite Resume Snippet", help="Click to get a professionally rewritten version"):
    if original_snippet:
        
        with st.spinner("Rewriting your snippet..."):
            
            rewritten_snippet = rewrite_resume_snippet(original_snippet)

        st.markdown("---")

        st.subheader("Original Snippet:")
        st.code(original_snippet, language="text") 

        st.subheader("Rewritten Snippet (AI-Enhanced):")
        st.success(rewritten_snippet) 

        st.markdown(
            """
            <style>
            .stCode {
                background-color: #f0f2f6;
                border-radius: 8px;
                padding: 15px;
                font-family: monospace;
                white-space: pre-wrap; /* Ensures text wraps within the code block */
            }
            .stSuccess {
                background-color: #e6ffe6;
                color: #1a5e20;
                border-left: 5px solid #4CAF50;
                border-radius: 8px;
                padding: 15px;
                font-weight: bold;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    else:
        
        st.warning("Please enter a resume snippet to rewrite.")

st.markdown("---")
st.info("Tip: For best results, provide a concise and specific snippet related to a single achievement or responsibility.")

