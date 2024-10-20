# meshmail by Joshua Hoffmann / 2024-10-20 / v1.0

import serial
import smtplib
import json
from email.mime.text import MIMEText
from datetime import datetime

with open('config.json') as config_file:
  config = json.load(config_file)

SERIAL_PORT = config['serial']['port']
BAUD_RATE = config['serial']['baudrate']
SMTP_SERVER = config['smtp']['server']
SMTP_PORT = config['smtp']['port']
SMTP_USER = config['smtp']['user']
SMTP_PASSWORD = config['smtp']['password']
DEFAULT_SENDER_NAME = config.get('default_sender', 'Mesh-Service')
LOG_FILE = "meshservice.log"

def log_message(message):
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  with open(LOG_FILE, "a") as log_file:
    log_file.write(f"{timestamp} - {message}\n")

def send_email(recipient, subject, content, sender_name=None):
  msg = MIMEText(content)
  msg['Subject'] = subject
  msg['From'] = f"{sender_name} <{SMTP_USER}>" if sender_name else f"{DEFAULT_SENDER_NAME} <{SMTP_USER}>"
  msg['To'] = recipient
  try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
      server.starttls()
      server.login(SMTP_USER, SMTP_PASSWORD)
      server.send_message(msg)
    log_message(f"Sent Mail successfully! {recipient}, Subject: {subject}, Content: {content}")
    print(f"{datetime.now()} - Sent Mail successfully! {recipient}")
  except Exception as e:
    log_message(f"Error while sending mail: {str(e)}")
    print(f"{datetime.now()} - Error while sending mail: {str(e)}")

def main():
  try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"{datetime.now()} - Serial output recognized, waiting for commands.")
  except Exception as e:
    print(f"{datetime.now()} - Error on serial output from the node: {str(e)}")
    log_message(f"Error on serial output from the node: {str(e)}")
    return

  recipient = None
  subject = None
  content = []
  sender_name = None
  node_name = None
  processing_message = False

  while True:
    line = ser.readline().decode('utf-8', errors='ignore').strip()
    if line:
      if "@mail" in line:
        processing_message = True
        content = []
        print(f"{datetime.now()} - Received message in the correct format. Processing.")
      if processing_message:
        if "to:" in line:
          recipient = line.split('to: ')[-1].strip()
          print(f"{datetime.now()} - to: {recipient}")
        elif "subject:" in line:
          subject = line.split('subject: ')[-1].strip()
          print(f"{datetime.now()} - subject: {subject}")
        elif "content:" in line:
          content.append(line.split('content: ')[-1].strip())
          print(f"{datetime.now()} - content: {content}")
        elif "from:" in line:
          sender_name = line.split('from: ')[-1].strip()
          print(f"{datetime.now()} - from: {sender_name}")
        elif "Node" in line and sender_name is None:
          # Funktioniert noch nicht so
          node_name = line.split('Node ')[-1].strip()
      if recipient and subject and content:
        send_email(recipient, subject, "\n".join(content), sender_name if sender_name else node_name)
        processing_message = False
        recipient = subject = sender_name = node_name = None
        content = []
          
if __name__ == '__main__':
  main()
