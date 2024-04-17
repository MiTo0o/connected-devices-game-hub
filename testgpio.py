import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

try:
    while True:
        # Iterate through all GPIO pins
        for pin in range(28):  # Adjust the range as needed based on your Pi model
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Use pull-down resistors
            pin_state = GPIO.input(pin)
            print(f"Pin {pin}: {'High' if pin_state else 'Low'}")

        time.sleep(0.1)  # Add a small delay to reduce CPU load

except KeyboardInterrupt:
    # Clean up GPIO
    GPIO.cleanup()
