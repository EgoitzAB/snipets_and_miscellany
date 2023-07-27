import smtplib

server = "smtp-mail.outlook.com"
port = 587

def prompt(string):
    """ Prompt to abstract the inputs """
    return input(string)

def collect_email_data():
    """ Email data collection and call to start proccess """
    password = prompt("Type your password and press enter: ")
    sender_email = prompt("From: ")
    receiver_email = prompt("To: ").split()
    message = prompt("Write the message body:")
    email_sender(password, sender_email, receiver_email, message)


def email_sender(sender_email, password, receiver_email, message):
    """ Email sending proccess with address verifier """
    try:
        with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            server.quit()
    except Exception as e:
        print(e)

collect_email_data()