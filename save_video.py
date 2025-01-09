import cv2
import time

# Open the camera feed
cap = cv2.VideoCapture(0)  # Use 0 for /dev/video0

if not cap.isOpened():
    print("Error: Camera not found or failed to open")
    exit()

# Define the codec and create a VideoWriter object to save the video
# 'XVID' codec and save as an .avi file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))  # Adjust resolution (640x480)

# Record for 5 seconds
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture")
        break

    # Write the frame to the video file
    out.write(frame)

    # Display the camera feed
    cv2.imshow("Camera Feed", frame)

    # Break the loop after 5 seconds
    if time.time() - start_time >= 5:
        break

    # Break if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything when done
cap.release()
out.release()
cv2.destroyAllWindows()
