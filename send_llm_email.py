# # import smtplib

# # email = input("SENDER EMAIL: ")
# # receiver_email = input("RECEIVER EMAIL: ")

# # subject = input("SUBJECT: ")
# # message = input("MESSAGE: ")

# # text = f"Subject: {subject}\n\n{message}"

# # server = smtplib.SMTP('smtp.gmail.com', 587)
# # server.starttls()

# # server.login(email, "sdznljbknpzslekp")

# # server.sendmail(email, receiver_email, text)

# # print("Email has to be sent to" + receiver_email)


# # from imap_tools import MailBox
# # from dotenv import load_dotenv
# # import os

# # username = os.getenv("RECEIVING_EMAIL_ADDRESS")
# # password = os.getenv("EMAIL_PASSWORD")

# # with MailBox("imap.gmail.com").login(username, password, "sd c")
 

# import smtplib
# import os
# from dotenv import load_dotenv
# from email.mime.text import MIMEText
# from email.header import Header
# from email.utils import formataddr

# # For LLM integration
# from litellm import completion

# # --- Load Environment Variables ---
# load_dotenv()

# SENDER_EMAIL = os.getenv("GMAIL_ADDRESS")
# GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL") # Get receiver email from .env

# # --- SMTP Configuration ---
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587 # Standard port for TLS

# # --- LLM Configuration ---
# LLM_MODEL = "gemini/gemini-pro" # Or "gemini/gemini-1.5-flash" if you have access

# def generate_email_content_with_llm(prompt_text):
#     """
#     Generates email subject and body using the Gemini LLM via LiteLLM.
#     The LLM response is expected to be in a specific format (e.g., "Subject: ...\n\nBody: ...").
#     """
#     if not GOOGLE_API_KEY:
#         print("Error: GOOGLE_API_KEY not found in environment variables. Cannot generate LLM content.")
#         return None, None

#     # Set the Google API key for LiteLLM
#     os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY # LiteLLM expects it in os.environ

#     llm_prompt = f"""You are an AI assistant tasked with generating a professional email.
#     Based on the following request: "{prompt_text}"

#     Generate a concise email with a clear subject line and a polite body.
#     Format your response like this:
#     Subject: [Your Generated Subject]
    
#     [Your Generated Email Body]
#     """
    
#     print("Generating email content with LLM...")
#     try:
#         response = completion(
#             model=LLM_MODEL,
#             messages=[{"role": "user", "content": llm_prompt}],
#             max_tokens=500, 
#             temperature=0.7 
#         )
#         llm_output = response.choices[0].message.content.strip()

#         # Parse the LLM output
#         if llm_output.startswith("Subject:"):
#             lines = llm_output.split('\n', 1) # Split only at the first newline
#             subject_line = lines[0].replace("Subject:", "").strip()
#             body_content = lines[1].strip() if len(lines) > 1 else ""
#             return subject_line, body_content
#         else:
#             print("LLM output format unexpected. Returning generic content.")
#             return "Automated Email (LLM Error)", f"Dear recipient,\n\nI apologize, but there was an issue generating this email content. Please disregard this message.\n\nSincerely,\nAutomated Bot"

#     except Exception as e:
#         print(f"Error calling LLM: {e}")
#         return "Automated Email (LLM Error)", f"Dear recipient,\n\nI apologize, but there was an issue generating this email content. Please disregard this message.\n\nSincerely,\nAutomated Bot"

# def send_llm_generated_email(receiver_email, subject, message_body):
#     """
#     Sends an email using the provided subject and message body.
#     """
#     if not SENDER_EMAIL or not GMAIL_APP_PASSWORD:
#         print("Error: SENDER_EMAIL or GMAIL_APP_PASSWORD not set. Cannot send email.")
#         return

#     try:
#         # Create the email message object
#         msg = MIMEText(message_body, 'plain', 'utf-8')
        
#         # Set proper headers for email clients
#         msg['From'] = formataddr((str(Header('Your Automated Assistant', 'utf-8')), SENDER_EMAIL)) # Customize sender name
#         msg['To'] = receiver_email
#         msg['Subject'] = Header(subject, 'utf-8')

#         # Connect to the SMTP server
#         with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#             server.starttls() # Secure the connection with TLS
#             server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
#             server.send_message(msg) # Use send_message for MIMEText objects

#         print(f"\nEmail successfully sent to {receiver_email}!")
#         print(f"Subject: {subject}")
#         print(f"Body snippet:\n{message_body[:200]}...")

#     except smtplib.SMTPAuthenticationError as e:
#         print(f"SMTP Authentication Error: {e}")
#         print("Please check your GMAIL_ADDRESS and GMAIL_APP_PASSWORD in the .env file.")
#         print("Ensure IMAP is enabled in your Gmail settings.")
#     except Exception as e:
#         print(f"An error occurred while sending the email: {e}")

# if __name__ == "__main__":
#     # Get a prompt from the user for the email content
#     email_prompt = input("What kind of email do you want to generate and send? (e.g., 'A thank you note for a recent meeting', 'An update on project status', 'An invitation to a webinar'):\n")

#     # Generate content using LLM
#     llm_subject, llm_message = generate_email_content_with_llm(email_prompt)

#     if llm_subject and llm_message:
#         # Send the generated email
#         send_llm_generated_email(RECEIVER_EMAIL, llm_subject, llm_message)
#     else:
#         print("Failed to generate email content. Email not sent.")


# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# print("=== Environment Variables Test ===")

# # Test each variable
# vars_to_check = ['GMAIL_ADDRESS', 'GMAIL_APP_PASSWORD', 'GOOGLE_API_KEY', 'RECEIVER_EMAIL']

# for var_name in vars_to_check:
#     value = os.getenv(var_name)
#     if value:
#         if var_name == 'GOOGLE_API_KEY':
#             print(f"✓ {var_name}: {value[:10]}... (length: {len(value)})")
#         elif var_name == 'GMAIL_APP_PASSWORD':
#             print(f"✓ {var_name}: {value[:4]}... (length: {len(value)})")
#         else:
#             print(f"✓ {var_name}: {value}")
#     else:
#         print(f"❌ {var_name}: Not found")

# # Check for common issues
# api_key = os.getenv('GOOGLE_API_KEY')
# if api_key:
#     print(f"\n--- API Key Analysis ---")
#     print(f"Starts with 'AIza': {api_key.startswith('AIza')}")
#     print(f"Length is 39: {len(api_key) == 39}")
#     print(f"Contains quotes: {'"' in api_key}")
    
#     if '"' in api_key:
#         print("⚠️  WARNING: API key contains quotes - remove them from .env file")


import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from litellm import completion

load_dotenv()

SENDER_EMAIL = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

LLM_MODEL = "gemini/gemini-1.5-flash"  
#LLM_MODEL = "gemini/gemini-pro"  # Use the pro model for better performance

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
    

    if not GEMINI_API_KEY.startswith('AIza'):  
        print("Warning: Google API key format seems unusual. Make sure you're using a Google AI Studio API key.")
    
    print("✓ All environment variables are set")
    print(f"✓ API Key: {GEMINI_API_KEY[:10]}... (length: {len(GEMINI_API_KEY)})")
    return True

def generate_email_content_with_llm(prompt_text):
    """
    Generates email subject and body using the Gemini LLM via LiteLLM.
    """
    if not GEMINI_API_KEY:  
        print("Error: GOOGLE_API_KEY not found in environment variables.")
        return None, None

    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

    # llm_prompt = f"""You are an AI assistant tasked with generating a professional email.
    # Based on the following request: "{prompt_text}"

    # Generate a concise email with a clear subject line and a polite body.
    # Format your response exactly like this:
    # Subject: [Your Generated Subject]
    
    # [Your Generated Email Body]
    # """
    
    print(f"Generating email content with LLM using model: {LLM_MODEL}...")
    try:
        response = completion(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": f"{prompt_text}"}],
            #max_tokens=500,
            #temperature=0.7
        )
        llm_output = response.choices[0].message.content.strip()
        print(f"✓ LLM response received: {len(llm_output)} characters")

        if "Subject:" in llm_output:
            lines = llm_output.split('\n', 1)
            subject_line = lines[0].replace("Subject:", "").strip()
            body_content = lines[1].strip() if len(lines) > 1 else ""
            return subject_line, body_content
        else:
            print("Warning: LLM output format unexpected.")
            print(f"Raw output: {llm_output[:200]}...")
            return "AI Generated Email", llm_output

    except Exception as e:
        print(f"Error calling LLM: {e}")
        print("This usually indicates an API key issue or network problem.")
        
        print("Trying alternative model: gemini/gemini-pro...")
        try:
            response = completion(
                model="gemini/gemini-pro",
                messages=[{"role": "user", "content": "Generate a thank you email for a recent meeting with a client."}],
                # max_tokens=500,
                # temperature=0.7
            )
            llm_output = response.choices[0].message.content.strip()
            print(f"✓ Alternative model worked! Response: {len(llm_output)} characters")
            
            if "Subject:" in llm_output:
                lines = llm_output.split('\n', 1)
                subject_line = lines[0].replace("Subject:", "").strip()
                body_content = lines[1].strip() if len(lines) > 1 else ""
                return subject_line, body_content
            else:
                return "AI Generated Email", llm_output
                
        except Exception as e2:
            print(f"Alternative model also failed: {e2}")
            return None, None

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
        return False
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        return False

if __name__ == "__main__":
    print("=== Email Automation Script ===")
    
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