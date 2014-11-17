from django.core.mail import send_mail, BadHeaderError

def send_user_message(subject, email, message):
    if subject and email and message:
        try:
            message = "Message from " + email + ": \n\n" + message
            send_mail(subject, message, email, ['lerus.chris@gmail.com'])
        except BadHeaderError:
            return "Invalid Header"
        #return "Fail"
    return "Your message has been successfuly sent. Thank you!"