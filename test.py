import RPi.GPIO as GPIO
import time

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the buttons
BUTTON_1_PIN = 17  # GPIO pin for button 1
BUTTON_2_PIN = 18  # GPIO pin for button 2
BUTTON_3_PIN = 22  # GPIO pin for button 3
BUTTON_4_PIN = 23  # GPIO pin for button 4

# Setup GPIO pins as inputs
GPIO.setup(BUTTON_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_4_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    # Main loop to test buttons
    while True:
        # Check if each button is pressed
        if GPIO.input(BUTTON_1_PIN) == GPIO.LOW:
            print("Button 1 pressed")
        if GPIO.input(BUTTON_2_PIN) == GPIO.LOW:
            print("Button 2 pressed")
        if GPIO.input(BUTTON_3_PIN) == GPIO.LOW:
            print("Button 3 pressed")
        if GPIO.input(BUTTON_4_PIN) == GPIO.LOW:
            print("Button 4 pressed")

        # Wait a short delay to debounce buttons
        time.sleep(0.1)

except KeyboardInterrupt:
    # Clean up GPIO on Ctrl+C exit
    GPIO.cleanup()
