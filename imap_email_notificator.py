import imaplib
import email
import RPi.GPIO as GPIO
import time

# GPIO config
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
buzzer_pin = 21
on = GPIO.LOW
off = GPIO.HIGH
GPIO.setup(21, GPIO.OUT)
GPIO.output(buzzer_pin, off)

# IMAP session establish
def get_imap_session(user_email, user_password):
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    M.login(user_email, user_password)
    return M


Mailbox = get_imap_session("", "")

temporary = 100

def is_email_important(message_number):
    assert isinstance(message_number, bytes), "Variable were passed in invalid type"
    typ, data = Mailbox.fetch(message_number, '(RFC822)')
    message = email.message_from_bytes(data[0][1])

    # Converting ugly string into pretty deliverer
    deliverer = message['From'].split()[1][1:-1]
    if deliverer == '':
        print("You received message from {someone_important} hope you are happy with that!".format(someone_important = deliverer))
        return True
    return False
    
try:
    while True:
        Mailbox.select()
        typ, data = Mailbox.search(None, 'ALL')
        num_messages = len(data[0].split())
        print("Messages in the mailbox: ", num_messages)
        if num_messages > temporary:
            # TODO - zrobic tak zeby zmienna num_messages przekonwertowac na bajty
            if is_email_important(data[0].split()[-1]):
                GPIO.output(buzzer_pin, on)
                time.sleep(1)
                GPIO.output(buzzer_pin, off)
                temporary = num_messages
                continue
        temporary = num_messages
        time.sleep(5)
except KeyboardInterrupt:
    Mailbox.close()
    Mailbox.logout()
    print("\nLogging out...")
    