import cv2
import time
from utils.capture_utils import open_camera, capture_frame, detect_face, draw_faces, generate_face_embeddings, release_camera
# from utils.storage_utils import 

def register_new_face():
    capture = open_camera()
    embeddings = None
    stable_start = None
    stable_duration = 2

    print("📷 Please look at the camera...")

    while True:
        frame = capture_frame(capture)
        face_locations = detect_face(frame)
        draw_faces(frame, face_locations)

        # Show video
        # cv2.imshow("Register Face", frame)

        if face_locations and embeddings is None:
            if stable_start is None:
                stable_start = time.time()
            elif time.time() - stable_start >= stable_duration:
                embeddings = generate_face_embeddings(frame, face_locations)
                if embeddings:
                    print("✅ Face embedding captured:", embeddings[0][:5])
                    print("👉 Press 'q' to quit")
                else:
                    print("⚠️ Face detected but no embeddings extracted")
        else:
            stable_start = None  # reset if face disappears

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    release_camera(capture)


if __name__ == '__main__':

    register_new_face()
