import board
import displayio
from adafruit_display_text import label
import terminalio
import time
import sys
import select  # For non-blocking I/O
import pwmio   # For buzzer

# Setup display
display = board.DISPLAY

# Create a display context (Group)
splash = displayio.Group()
display.root_group = splash

# Initialize variables
text_lines = []
current_y = 10  # Start a bit lower from the top
max_lines = 10  # Adjust based on your display size
line_height = 20  # Increased for better readability

# Define constants for buzzer
OFF = 0
ON = 2 ** 15


# Set up the buzzer
buzzer = pwmio.PWMOut(board.BUZZER, variable_frequency=True)

def buzz():
    """Make the buzzer sound."""
    buzzer.frequency = 4000  # Set frequency to 4000 Hz
    buzzer.duty_cycle = ON   # Turn on the buzzer
    time.sleep(0.05)          # Beep for half a second
    buzzer.duty_cycle = OFF  # Turn off the buzzer

def add_text(new_text):
    global current_y
    
    # If we've reached the maximum number of lines, remove the oldest line
    if len(text_lines) >= max_lines:
        oldest_line = text_lines.pop(0)
        splash.remove(oldest_line)
        
        # Move existing lines up
        for line in text_lines:
            line.y -= line_height
    
    # Create a new text label
    text_area = label.Label(
        terminalio.FONT, 
        text=new_text, 
        color=0xFFFFFF,
        x=10,
        y=current_y + (line_height * len(text_lines))
    )
    
    splash.append(text_area)
    text_lines.append(text_area)

def read_input():
    # Check if there is input available
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        try:
            received = sys.stdin.readline().strip()  # Read a line from stdin
            if received:
                add_text(received)
                # Trigger buzzer when receiving a buzz command
                if "Buzz" in received:
                    buzz()
        except Exception as e:
            add_text(f"Error: {str(e)}")

# Main loop
while True:
    read_input()  # Call the function to read input
    time.sleep(0.05)  # Keep this short to maintain responsiveness
