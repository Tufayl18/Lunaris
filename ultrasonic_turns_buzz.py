import RPi.GPIO as GPIO
import time
import serial  # Import serial library


# GPIO pin setup for motors
IN1 = 17  # Motor 1 control pin 1 (right wheel)
IN2 = 27  # Motor 1 control pin 2 (right wheel)
IN3 = 22  # Motor 2 control pin 1 (left wheel)
IN4 = 23  # Motor 2 control pin 2 (left wheel)
ENA = 5   # Motor 1 enable (PWM control)
ENB = 6   # Motor 2 enable (PWM control)

# GPIO pin setup for ultrasonic sensors
TRIG_LEFT = 24  # Trigger pin for left ultrasonic sensor
ECHO_LEFT = 25  # Echo pin for left ultrasonic sensor
TRIG_RIGHT = 18  # Trigger pin for right ultrasonic sensor
ECHO_RIGHT = 12  # Echo pin for right ultrasonic sensor

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup motor pins
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

# Setup ultrasonic sensor pins
GPIO.setup(TRIG_LEFT, GPIO.OUT)
GPIO.setup(ECHO_LEFT, GPIO.IN)
GPIO.setup(TRIG_RIGHT, GPIO.OUT)
GPIO.setup(ECHO_RIGHT, GPIO.IN)

# PWM frequency
pwm_freq = 1000  # Hz

# Setup PWM for motor speed control
pwmA = GPIO.PWM(ENA, pwm_freq)
pwmB = GPIO.PWM(ENB, pwm_freq)


normal_speed = 10  # Adjust this for normal speed (e.g., 10%)
turning_speed = 20  # Increase this value for turning (e.g., 50%)

# Start motors at 50% speed
pwmA.start(normal_speed)  # 50% duty cycle for motor 1 (right wheel)
pwmB.start(normal_speed)  # 50% duty cycle for motor 2 (left wheel)

# Initialize serial communication with Wio Terminal
ser = serial.Serial('/dev/ttyACM0', 115200)  # Adjust '/dev/serial0' as necessary

# Function to send messages to Wio Terminal
def send_message(message):
    ser.write(f"{message}\n".encode())  # Send the message followed by a newline

# Function to move both motors forward
def move_forward():
	pwmA.ChangeDutyCycle(normal_speed)
	pwmB.ChangeDutyCycle(normal_speed)
	
	GPIO.output(IN1, GPIO.HIGH)  # Right wheel forward
	GPIO.output(IN2, GPIO.LOW)
	GPIO.output(IN3, GPIO.HIGH)  # Left wheel forward
	GPIO.output(IN4, GPIO.LOW)
	send_message("Moving forward")  # Send message

# Function to move motors for a right turn
def turn_right():
	
	pwmA.ChangeDutyCycle(turning_speed)  # Increase right wheel speed
	pwmB.ChangeDutyCycle(turning_speed)  # Increase left wheel speed
	
	GPIO.output(IN1, GPIO.LOW)   # Right wheel backward
	GPIO.output(IN2, GPIO.HIGH)
	GPIO.output(IN3, GPIO.HIGH)  # Left wheel forward
	GPIO.output(IN4, GPIO.LOW)
	send_message("Buzz : Turning Right")  # Send message
    #send_message("Object detected on left, turning right")
    
# Function to move motors for a left turn
def turn_left():
	
	pwmA.ChangeDutyCycle(turning_speed)  # Increase right wheel speed
	pwmB.ChangeDutyCycle(turning_speed)  # Increase left wheel speed
    
	GPIO.output(IN1, GPIO.HIGH)  # Right wheel forward
	GPIO.output(IN2, GPIO.LOW)
	GPIO.output(IN3, GPIO.LOW)   # Left wheel backward
	GPIO.output(IN4, GPIO.HIGH)
	send_message("Buzz : Turning Left")  # Send message
    #send_message("Object detected on right, turning left")
    
# Function to measure distance using an ultrasonic sensor
def measure_distance(trig, echo):
    # Send trigger pulse
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    pulse_start = time.time()

    # Wait for echo response
    while GPIO.input(echo) == 0:
        pulse_start = time.time()

    pulse_end = time.time()

    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    # Calculate pulse duration and convert to distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound: 343m/s
    return distance

# Main loop
try:
    while True:
        distance_left = measure_distance(TRIG_LEFT, ECHO_LEFT)
        distance_right = measure_distance(TRIG_RIGHT, ECHO_RIGHT)
        
        # Send distance measurements to Wio Terminal
        #send_message(f"Left Distance: {distance_left:.2f} cm, Right Distance: {distance_right:.2f} cm")

        if distance_left < 15:  # Object detected on left side
            turn_right()
        elif distance_right < 15:  # Object detected on right side
            turn_left()
        else:
            move_forward()  # Move forward

        time.sleep(0.1)  # Short delay to avoid excessive checking

except KeyboardInterrupt:
    # Cleanup on Ctrl+C exit
    pass

finally:
    # Stop the motors and clean up
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()

