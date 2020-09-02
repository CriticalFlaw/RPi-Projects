# CAT FEEDER SCRIPT

import RPi.GPIO as GPIO
import time

# Setup the Servo GPIO
ServoPin=18
GPIO.setwarnings(False)

# Setup the GPIO library to work with the servo
GPIO.setmode(GPIO.BCM)
GPIO.setup(ServoPin, GPIO.OUT)

try:
  print "Dispencing food..."
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
  print "Done!"
