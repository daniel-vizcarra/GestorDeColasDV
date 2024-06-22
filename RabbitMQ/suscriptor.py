import pika
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_email(subject, body, to_email):
    from_email = "daniel.a.vizcarra@outlook.com"
    from_password = "150444bC$"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

def callback(ch, method, properties, body):
    message = body.decode()
    print(f" [x] Received {message}")
    
    # Check if current date is June 22, 2024
    current_date = datetime.now().date()
    target_date = datetime(2024, 6, 22).date()  # June 22, 2024

    if current_date == target_date:
        send_email("Ecuador vs Venezuela 5PM", message, "sirdanvizcarra@gmail.com")
    else:
        print("It's not June 22, 2024 yet.")

def receive_message(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    queue_name = 'email_queue'
    receive_message(queue_name)
