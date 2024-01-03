import json
import pika
import smtplib
from email.mime.text import MIMEText
from decouple import config

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config('EMAIL_USERNAME')
    msg['To'] = to_email

    with smtplib.SMTP(config('SMTP_SERVER'), config('SMTP_PORT')) as server:
        server.starttls()
        server.login(config('EMAIL_USERNAME'), config('EMAIL_PASSWORD'))
        server.sendmail(config('EMAIL_USERNAME'), to_email, msg.as_string())

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

email_data = {
    'to': 'recipient@example.com',
    'subject': 'Test Subject',
    'body': 'This is a test email body.'
}

channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(email_data))

print(f" [x] Sent email data to the queue")

connection.close()