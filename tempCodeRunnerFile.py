import cv2
from utils.capture_utils import open_camera, capture_frame, show_frame, detect_face, release_camera
print("testinggggg")
def register_new_face():
    capture = open_camera()
    while True:
        frame = capture_frame(capture)
        show_frame("Register Face", frame)
        detect_face(capture, frame)
        key = cv2.waitKey(10) & 0xFF
        if key == ord('q') or key == 27: #esc key 
            break
    release_camera(capture)

register_new_face()