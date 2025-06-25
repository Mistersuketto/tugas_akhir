import cv2

cam = cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Display the original and HSV frames
    cv2.imshow('Original Frame', frame)
    cv2.imshow('HSV Frame', hsv_frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the camera and close all OpenCV windows
cam.release()
cv2.destroyAllWindows()