import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"


context = ssl.create_default_context()
def notify_arrival(pkg_name,dest_mail):
    try:

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            sender_email = "lidaniel568@gmail.com"  # Enter your address
            password = "7_password"  # input("Type your password and press enter: ")
            message = f'Your {pkg_name} has been delivered to your doorstep!'
            server.login(sender_email, password)
            server.sendmail(sender_email, dest_mail, message)
    except smtplib.SMTPAuthenticationError:
        print("Couldn't send email notification")

