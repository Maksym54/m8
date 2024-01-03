import json
import pika
import smtplib
from email.mime.text import MIMEText
from decouple import config

def send_email(email_data):
    msg = MIMEText(email_data['body'])
    msg['Subject'] = email_data['subject']
    msg['From'] = config('EMAIL_USERNAME')
    msg['To'] = email_data['to']

    with smtplib.SMTP(config('SMTP_SERVER'), config('SMTP_PORT')) as server:
        server.starttls()
        server.login(config('EMAIL_USERNAME'), config('EMAIL_PASSWORD'))
        server.sendmail(config('EMAIL_USERNAME'), email_data['to'], msg.as_string())

def callback(ch, method, properties, body):
    email_data = json.loads(body.decode('utf-8'))
    send_email(email_data)
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')
channel.basic_consume(queue='email_queue', on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()