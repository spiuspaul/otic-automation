from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

google_api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5, api_key=google_api_key)

template = PromptTemplate.from_template(
    """Rewrite the following resume snippet to be more professional, clear, concise, and impactful.
Focus on using strong action verbs and quantifying achievements where possible.

Original Snippet:
{resume_snippet}

Rewritten Snippet:
"""
)

chain = template | llm

def rewrite_resume_snippet(resume_snippet: str) -> str:
    """
    Rewrites a given resume snippet to be more professional using an LLM.

    Args:
        resume_snippet: The original resume text snippet to be rewritten.

    Returns:
        The professionally rewritten resume snippet.
    """
    
    response = chain.invoke({"resume_snippet": resume_snippet})
    return response.content


if __name__ == "__main__":
    
    example_snippet = "Managed social media accounts. Posted daily content."
    rewritten_example = rewrite_resume_snippet(example_snippet)
    print("Original:", example_snippet)
    print("Rewritten:", rewritten_example)

    example_snippet_2 = "Responsible for customer support, handling calls and emails."
    rewritten_example_2 = rewrite_resume_snippet(example_snippet_2)
    print("\nOriginal:", example_snippet_2)
    print("Rewritten:", rewritten_example_2)
