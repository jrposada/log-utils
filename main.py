import subprocess
import smtplib
from email.mime.text import MIMEText
import apache_log_parser

def send_email(data):
    print('TODO', data)
    # sender_email = "your_email@gmail.com"
    # receiver_email = "recipient_email@example.com"
    # smtp_server = "smtp.gmail.com"
    # smtp_port = 587
    # smtp_username = "your_email@gmail.com"
    # smtp_password = "your_email_password"

    # msg = MIMEText(message)
    # msg['Subject'] = subject
    # msg['From'] = sender_email
    # msg['To'] = receiver_email

    # with smtplib.SMTP(smtp_server, smtp_port) as server:
    #     server.starttls()
    #     server.login(smtp_username, smtp_password)
    #     server.send_message(msg)

def is_invalid(data):
    if data['request_method'] not in ['GET', 'POST', 'PUT', 'OPTIONS']:
        return True

    return False

def monitor_log():
    # log_file = "/var/log/nginx/access.log"
    log_file = "./.mock-data/access.log"

    # Initialize the parser with the log format.
    log_format = '%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"'
    parser = apache_log_parser.make_parser(log_format)

    with subprocess.Popen(['tail', '-F', log_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        while True:
            log_line = proc.stdout.readline().decode('utf-8').strip()
            parsed_data = parser(log_line)

            if is_invalid(parsed_data):
                send_email(parsed_data)

if __name__ == "__main__":
    monitor_log()
