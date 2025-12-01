import cv2
print("Starting webcam")
capture = cv2.VideoCapture(0)
if not capture.isOpened():
    print("Error: Could not open webcam")
    exit()
else:
    print("✅ Webcam opened successfully")

while True:
    return_value, frame = capture.read()
    print("Read status:", return_value) 
    if not return_value:
        print("❌ Failed to grab frame")
        break

    cv2.imshow("Webcam View", frame)
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()