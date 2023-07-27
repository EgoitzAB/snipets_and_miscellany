import smtplib, ssl
import re

# getpass para las contraseñas
port = 25 #SSL

def prompt(prompt):
    """ Automatic prompt """
    return input(prompt).strip()

def collect_email_data():
    """ Email data collection and call to start proccess """
    password = prompt("Type your password and press enter: ")
    sender_email = prompt("From: ")
    receiver_email = prompt("To: ").split()
    message = prompt("Write the message body:")
    email_sender(password, sender_email, receiver_email, message)


def email_sender(password, sender_email, receiver_email, message):
    """ Email sending proccess with address verifier """
    try:
        with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
            server.connect("smtp-mail.outlook.com", 587)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            server.quit()
    except Exception as e:
        print(e)
    
collect_email_data()
