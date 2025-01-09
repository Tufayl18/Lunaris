import cv2

cap = cv2.VideoCapture(-1)  # Change -1 to 0 to access /dev/video0

if not cap.isOpened():
    print("Error: Camera not found or failed to open")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture")
        break

    cv2.imshow("Camera Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
