import cv2
import face_recognition

def open_camera(camera_index=0):
    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        raise Exception("❌ Error: Could not open webcam")
    print("✅ Webcam opened successfully")
    return capture

def capture_frame(capture):
    return_value, frame = capture.read() 
    if not return_value:
        print("❌ Failed to grab frame")
        raise Exception("Failed to grab frame")
    return frame

# def show_frame(window_name, frame):
#     cv2.imshow(window_name, frame)

def detect_face(frame):
    """Return face locations in (top, right, bottom, left) format"""
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
    face_locations = face_recognition.face_locations(rgb_frame, model="hog") 
    return face_locations

def draw_faces(frame, face_locations):
    """Draw rectangles on detected faces (optional UI/debug)"""
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 0), 2)
    cv2.imshow("Face Detection", frame)

def generate_face_embeddings(frame, face_locations):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Adding num_jitters=3 forces the engine to recalculate the face 3 times 
    # to capture highly specific micro-details (crucial for telling siblings apart)
    face_embeddings = face_recognition.face_encodings(rgb_frame, face_locations, num_jitters=3)
    return face_embeddings

def release_camera(capture):
    capture.release()
    cv2.destroyAllWindows()