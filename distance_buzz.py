import RPi.GPIO as GPIO
import time
import serial

# GPIO pin setup for ultrasonic sensor
TRIG = 24  # GPIO pin connected to the TRIG pin of the sensor
ECHO = 25  # GPIO pin connected to the ECHO pin of the sensor

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup ultrasonic sensor pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Initialize serial communication with the Wio Terminal
ser = serial.Serial('/dev/ttyACM0', 115200)  # Change to the correct serial port

def measure_distance():
    # Ensure the trigger pin is low
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.2)  # Small delay to stabilize the sensor
    
    # Send a 10 microsecond pulse to trigger
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)  # 10 microsecond pulse
    GPIO.output(TRIG, GPIO.LOW)
    
    # Wait for the echo to be received
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()  # Save the start time

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()  # Save the end time

    # Calculate pulse duration and convert it to distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is 34300 cm/s, divide by 2 for round trip
    distance = round(distance, 2)  # Round to 2 decimal places
    return distance

try:
    while True:
        distance = measure_distance()
        # Send the distance measurement to the Wio Terminal
        ser.write(f"Moving Forward\n".encode('utf-8'))
        print(f"Distance: {distance} cm\n")
        time.sleep(1)  # Wait for 1 second before measuring again

except KeyboardInterrupt:
    # Cleanup on Ctrl+C exit
    GPIO.cleanup()
    ser.close()  # Close the serial connection

