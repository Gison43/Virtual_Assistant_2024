import smtplib
from email.mime.text import MIMEText

def send_text_via_email(phone_number, message):
   to_number = f"{6138169713}@sms.fido.ca"

   from_email = "gc519@ncf.ca"
   from_password = "Daisydo1612"

   smtp_server = "smtp.ncf.ca"
   smtp_port = 587

   msg = MIMEText(message)
   msg["From"] = from_email
   msg["To"] = to_number
   msg["Subject"] = "Message from your virtual assistant"

   try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
           server.starttls() #start tls encryption
           server.login(from_email, from_password)
           server.sendmail(from_email, to_number, msg.as_string())
        print("Text message sent successfully!")
   except Exception as e:
        print(f"Failed to send message: {e}")


if __name__ == "__main__":
   phone_number = "6138169713"
   message = "Hello this is s a test"
   send_text_via_email(phone_number, message)
