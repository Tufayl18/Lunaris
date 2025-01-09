from flask import Flask, Response, request
import cv2

app = Flask(__name__)

# Open camera on Raspberry Pi
camera = cv2.VideoCapture(-1)  # 0 for Pi cam, adjust for USB cam if needed

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Return the frame in byte format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Endpoint to receive confirmation message from the laptop
@app.route('/processing_done', methods=['POST'])
def processing_done():
    # Process the message from laptop (you can also pass data here if needed)
    data = request.json
    print(f"Received message from laptop: {data['message']}")
    return "Message received"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
