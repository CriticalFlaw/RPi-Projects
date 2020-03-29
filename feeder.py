# CAT FEEDER SCRIPT

# Get the date time libraries
import time
from datetime import date, timedelta, datetime
from astral import *
from pytz import timezone

# Get the SMTP email library
import smtplib

# Get the Pi GPIO library
import RPi.GPIO as GPIO

# Setup the sender and receiver emails
email_to = 'email@you.com'
email_gmail_user = 'user@domain.tv'
email_gmail_pwd = 'verysecretandsecurepassword'

# Setup the location and lat/lon for our calculations
a = Astral()
location = a['Ottawa']

# Setup the Servo GPIO
ServoPin=18
GPIO.setwarnings(False)

# Setup the email sender
def send_email(feedtime):
  fedtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  to = email_to
  gmail_user = email_gmail_user
  gmail_pwd = email_gmail_pwd
  smtpserver = smtplib.SMTP("smtp.gmail.com",587)
  smtpserver.ehlo()
  smtpserver.starttls()
  smtpserver.ehlo
  smtpserver.login(gmail_user, gmail_pwd)
  header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: CatFeeder: Leo has been successfully fed! \n'
  #print header
  msg = header + '\nLeo was fed on ' + fedtime + '.\n\nNext feeding time is ' + feedtime + '.\n\n'
  #print msg
  smtpserver.sendmail(gmail_user, to, msg)
  smtpserver.close()

# SERVO ROTATION FUNCTION
def feed():
  # Setup the GPIO library to work with the servo
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(ServoPin, GPIO.OUT)

  try:
    servo = GPIO.PWM(ServoPin, 50)
    servo.start(12.5)

    # Rotate left, right, then left again rather than in a continuous circle to prevent the food from jamming the servo
    servo.ChangeDutyCycle(7.5)
    time.sleep(0.8)
    servo.ChangeDutyCycle(2.5)
    time.sleep(0.8)
    servo.ChangeDutyCycle(7.5)
    time.sleep(0.8)

  finally:
    # Clean up after rotation
    servo.stop()
    GPIO.cleanup()

def getfeedtime():
  time = datetime.now()
  morning = time.replace(hour=7, minute=0,second=0)
  evening = time.replace(hour=17, minute=0,second=0)
  # Determine the next feeding time
  if time < morning and time < evening:
    time = morning
  elif time > morning and time < evening:
    time = evening
  elif time > morning and time > evening:
    time = morning + timedelta(days=1)
  return time.strftime("%Y-%m-%d %H:%M:%S")

# Get the first feeding time
feedtime = getfeedtime()
print "First feeding session is on %s" % feedtime

# MAIN CAT FEEDER LOOP
while True:
  # Get the current time
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  # Compare time values. If there's a match then dispense food, otherwise keep looping.
  if now == feedtime:
    # Set the time varaible for when we send the notification email.
    feedtime=datetime.now(timezone('US/Central'))
    print "Leo Feeding Time! Dispensing food..."
    time.sleep(5)
    feed()
    # Get the next feeding time
    feedtime = getfeedtime()
    # Send the email
    print "Sending the email notification..."
    time.sleep(5)
    send_email(feedtime)
    print "Next feeding session is on %s" % feedtime

  # Update the feeding time each day
  if time.strftime("%H") == "03" and time.strftime("%M") == "01" and time.strftime("%S") == "01":
    feedtime = getfeedtime()

  # If there's nothing to do, reset to the loop...
  time.sleep(1)
