import imaplib
import email

# --- Lab Configuration ---
NCF_SERVER = "mail.ncf.ca"
NCF_USER = "gc519@ncf.ca"
NCF_PASS = "Daisydo1612"
MY_EMAIL = "l_periard@yahoo.ca" # Your 'Public Mobile' sender address

def listen_for_signal():
    try:
        # 1. Connect to the 'Auditory Cortex'
        mail = imaplib.IMAP4_SSL(NCF_SERVER)
        mail.login(NCF_USER, NCF_PASS)
        mail.select("inbox")

        # 2. Search for UNREAD emails from YOU
        # Format: (FROM "email" UNSEEN)
        search_criterion = f'(FROM "{MY_EMAIL}" UNSEEN)'
        status, data = mail.search(None, search_criterion)

        if status == 'OK':
            mail_ids = data[0].split()
            if not mail_ids:
                print("No new signals detected...")
                return

            for num in mail_ids:
                # 3. Fetch the 'Envelope' (the headers)
                status, msg_data = mail.fetch(num, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = msg['subject']
                        print(f"Signal Received! Command: {subject}")
                        
                        # Mark as read is automatic with (RFC822) fetch on most servers
        
        mail.logout()

    except Exception as e:
        print(f"Auditory failure: {e}")

if __name__ == "__main__":
    print("VA is listening... send an email to your NCF account now.")
    listen_for_signal()
