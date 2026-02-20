import smtplib
from email.mime.text import MIMEText

# --- Lab Configuration ---
NCF_USER = "gc519@ncf.ca"  # Replace with your NCF username
NCF_PASS = "Daisydo1612"          # Replace with your NCF password
DESTINATION = "6138169713@msg.telus.com"

def send_signal(content):
    try:
        # 1. Create the 'Mime' container (Plain Text only for SMS)
        msg = MIMEText(content)
        msg['From'] = NCF_USER
        msg['To'] = DESTINATION
        msg['Subject'] = "VA Alert" # Most gateways ignore subjects, but we include it

        # 2. Connect to the NCF 'Nervous System'
        # NCF uses SSL on port 465 or STARTTLS on port 587. Let's try SSL first.
        print("Connecting to NCF servers...")
        with smtplib.SMTP_SSL("mail.ncf.ca", 465) as server:
            server.login(NCF_USER, NCF_PASS)
            
            # 3. Discharge the signal
            server.send_message(msg)
            
        print("Signal sent successfully! Check your phone.")
        
    except Exception as e:
        print(f"Signal failure: {e}")

if __name__ == "__main__":
    send_signal("Hello Scientist! This is your VA reporting from the Pi.")
