import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def email_alert(subject, body, to, attachments=None):
    print("Attachments:", attachments)  # Print out the attachments variable for debugging

    sender_email = "sigurietedhenave@gmail.com"
    password = "xdou safz vqat jvsb"  # Replace with a secure method of storing passwords

    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to

    if attachments:
        for attachment_filename in attachments:
            part = MIMEBase('application', 'octet-stream')
            with open(attachment_filename, 'rb') as file:
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {attachment_filename}')
            msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, to, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
    finally:
        server.quit()
