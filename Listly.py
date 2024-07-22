import imaplib
import email
# import pandas as pd
from multion.client import MultiOn
import agentops

multion = MultiOn(api_key="xxx", agentops_api_key="xxx")

browse = multion.retrieve(
    cmd="Find the latest emails with the sender subject and time sent and prioritize them",
    url="https://mail.google.com/mail/u/0/#inbox",
    local=True,
    fields=['sender, subject, time sent']
)

print("Browse response:", browse)

# click into each email 
# retrieve the text that has highest priority 
# identify the keywords and reorder

def fetch_emails():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('hackathonemail8@gmail.com', 'hackathonlogin!')
    mail.select('inbox')
    
    status, data = mail.search(None, 'ALL')
    email_ids = data[0].split()
    
    emails = []
    
    for email_id in email_ids:
        status, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        email_data = {
            'from': msg['from'],
            'subject': msg['subject'],
            'date': msg['date'],
            'body': ''
        }
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    email_data['body'] += part.get_payload(decode=True).decode()
        else:
            email_data['body'] = msg.get_payload(decode=True).decode()
        
        emails.append(email_data)
    
    mail.logout()
    return emails

def prioritize_emails(emails):
    priority_list = []
    
    for email in emails:
        priority_score = 0
        
        if 'urgent' in email['subject'].lower():
            priority_score += 10
        if 'boss@example.com' in email['from']:
            priority_score += 5
        
        priority_list.append({
            'from': email['from'],
            'subject': email['subject'],
            'date': email['date'],
            'body': email['body'],
            'priority_score': priority_score
        })
    
    priority_list = sorted(priority_list, key=lambda x: x['priority_score'], reverse=True)
    return priority_list

def generate_csv(priority_list, file_path='email_priority_list.csv'):
    # df = DataFrame(priority_list)
    df.to_csv(file_path, index=False)

# emails = fetch_emails()
# priority_list = prioritize_emails(emails)
# generate_csv(priority_list)
