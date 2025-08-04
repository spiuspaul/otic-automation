import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# --- Langchain specific imports ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser 

load_dotenv()

SENDER_EMAIL = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY 

LLM_MODEL = "gemini-1.5-flash" 

def validate_environment():
    """Validate that all required environment variables are set."""
    missing_vars = []
    
    if not SENDER_EMAIL:
        missing_vars.append("GMAIL_ADDRESS")
    if not GMAIL_APP_PASSWORD:
        missing_vars.append("GMAIL_APP_PASSWORD")
    if not GEMINI_API_KEY: 
        missing_vars.append("GEMINI_API_KEY")
    if not RECEIVER_EMAIL:
        missing_vars.append("RECEIVER_EMAIL")
    
    if missing_vars:
        print(f"Error: Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file and ensure all required variables are set.")
        return False
    
    if GEMINI_API_KEY and GEMINI_API_KEY.startswith('AIza'): 
        print("WARNING: Your Google API key format starts with 'AIza'.")
        print("This usually indicates it's a key from Google Cloud Console, not Google AI Studio.")
        print("For Gemini models with Langchain, it's highly recommended to use a key specifically generated from Google AI Studio (aistudio.google.com).")
        print("If you still face 'API key not valid' errors, generate a new key from aistudio.google.com.")
    
    print("✓ All environment variables are set")
    print(f"✓ API Key: {GEMINI_API_KEY[:10]}... (length: {len(GEMINI_API_KEY)})")
    return True

def generate_email_content_with_llm(prompt_text):
    """
    Generates email subject and body using the Gemini LLM via Langchain.
    """
    if not GEMINI_API_KEY: 
        print("Error: GEMINI_API_KEY not found in environment variables. Cannot generate LLM content.")
        return None, None

    print(f"Generating email content with LLM using Langchain and model: {LLM_MODEL}...")
    try:

        llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0.7) 
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI assistant tasked with generating a professional email. Your output should contain both the subject and the body. Format your response clearly."),
            ("user", f"Based on the following request: \"{prompt_text}\"\n\nGenerate a concise email with a clear subject line and a polite body.\nFormat your response exactly like this:\nSubject: [Your Generated Subject]\n\n[Your Generated Email Body]")
        ])
        
        chain = prompt | llm | StrOutputParser()

        llm_output = chain.invoke({"prompt_text": prompt_text})
        llm_output = llm_output.strip() 
        
        print(f"✓ LLM response received: {len(llm_output)} characters")

        subject_line = "AI Generated Email (No Subject Found)"
        body_content = llm_output

        if "Subject:" in llm_output:
            lines = llm_output.split('\n', 1) 
            if len(lines) > 0 and lines[0].strip().startswith("Subject:"):
                subject_line = lines[0].replace("Subject:", "").strip()
                body_content = lines[1].strip() if len(lines) > 1 else ""
            else:
                print("Warning: 'Subject:' found but not at the beginning of the first line or not followed by content.")
        else:
            print("Warning: LLM output format unexpected. 'Subject:' not found. Using raw output as body.")
        
        return subject_line, body_content

    except Exception as e:
        print(f"Error calling LLM via Langchain: {e}")
        print("This usually indicates an API key issue, model unavailability, or network problem.")
        return "AI Generated Email (Error)", "Dear recipient,\n\nI apologize, but there was an issue generating this email content using the LLM. Please try again later.\n\nSincerely,\nAutomated Bot"

def send_llm_generated_email(receiver_email, subject, message_body):
    """
    Sends an email using the provided subject and message body.
    """
    if not SENDER_EMAIL or not GMAIL_APP_PASSWORD:
        print("Error: Email credentials not set. Cannot send email.")
        return False

    try:
        msg = MIMEText(message_body, 'plain', 'utf-8')
        
        msg['From'] = formataddr((str(Header('Your Automated Assistant', 'utf-8')), SENDER_EMAIL))
        msg['To'] = receiver_email
        msg['Subject'] = Header(subject, 'utf-8')

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        print(f"\n✓ Email successfully sent to {receiver_email}!")
        print(f"Subject: {subject}")
        print(f"Body snippet:\n{message_body[:200]}...")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
        print("Please check your GMAIL_ADDRESS and GMAIL_APP_PASSWORD in the .env file.")
        print("Ensure App Passwords are enabled and IMAP is enabled in your Gmail settings.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while sending the email: {e}")
        return False

if __name__ == "__main__":
    print("=== Email Automation Script (Using Langchain) ===")
    
    if not validate_environment():
        print("\nPlease fix the environment variable issues before running the script.")
        exit(1)
    
    email_prompt = input("\nWhat kind of email do you want to generate and send? (e.g., 'A thank you note for a recent meeting', 'An update on project status', 'An invitation to a webinar'):\n")
    llm_subject, llm_message = generate_email_content_with_llm(email_prompt)

    if llm_subject and llm_message:
        print(f"\n--- Generated Email Content ---")
        print(f"Subject: {llm_subject}")
        print(f"Body:\n{llm_message}")
        
        confirm = input("\nDo you want to send this email? (y/n): ")
        if confirm.lower() == 'y':
            send_llm_generated_email(RECEIVER_EMAIL, llm_subject, llm_message)
        else:
            print("Email not sent.")
    else:
        print("Failed to generate email content. Email not sent.")



