import cv2
import time
import datetime
import numpy as np
import face_recognition
from utils.capture_utils import (
    open_camera, capture_frame, detect_face, 
    generate_face_embeddings, release_camera
)
from utils.storage_utils import get_all_users, get_embeddings_for_user, mark_attendance

def load_known_faces():
    print("🔓 Decrypting and caching facial profiles from database...")
    known_users = []
    db_users = get_all_users()
    
    for user_id, name, reg_no in db_users:
        embedding = get_embeddings_for_user(user_id)
        if embedding is not None:
            # FORCE convert to standard 1D float64 numpy array
            embedding_np = np.array(embedding, dtype=np.float64).flatten()
            known_users.append({
                "id": user_id,
                "name": name,
                "reg_no": reg_no,
                "embedding": embedding_np
            })
            
    print(f"✅ Loaded {len(known_users)} biometric profiles successfully.")
    return known_users

def mark_attendance_workflow():
    print("\n" + "═"*40)
    print("✅ BIOCRYPT - ATTENDANCE VERIFICATION")
    print("═"*40)
    
    known_users = load_known_faces()
    if not known_users:
        print("⚠️ System Alert: No registered students found in database.")
        return

    try:
        capture = open_camera()
    except Exception as e:
        print(f"❌ Camera Error: {e}")
        return

    print("\n🎥 Scanning... Look directly into the lens. Press 'q' to abort.")
    
    # ─── SECURITY PARAMETERS ──────────────────────────────────────────
    STRICT_THRESHOLD = 0.38  # Strict cutoff to block sibling lookalikes
    TIMEOUT_DURATION = 10.0  # Maximum seconds allowed to authenticate
    # ──────────────────────────────────────────────────────────────────
    
    start_time = time.time()  # Start the clock right here
    attendance_marked = False
    timeout_triggered = False

    while True:
        # 1. Calculate elapsed time on every single frame loop iteration
        elapsed_time = time.time() - start_time
        time_left = max(0.0, TIMEOUT_DURATION - elapsed_time)

        if elapsed_time >= TIMEOUT_DURATION:
            timeout_triggered = True
            break  # Break out of the infinite loop immediately!

        try:
            frame = capture_frame(capture)
        except Exception:
            break

        face_locations = detect_face(frame)
        live_embeddings = generate_face_embeddings(frame, face_locations)

        # Make a clear mutable copy of the frame to draw our UI countdown overlay
        display_frame = frame.copy()

        if face_locations and live_embeddings:
            for i, (top, right, bottom, left) in enumerate(face_locations):
                if i >= len(live_embeddings):
                    continue
                
                live_emb = np.array(live_embeddings[i], dtype=np.float64).flatten()
                box_color = (0, 0, 255) 
                display_name = f"SCANNING... ({time_left:.1f}s left)"

                known_embeddings_list = [user["embedding"] for user in known_users]
                
                if known_embeddings_list:
                    distances = face_recognition.face_distance(known_embeddings_list, live_emb)
                    
                    if len(distances) > 0:
                        best_match_idx = distances.argmin()
                        current_distance = distances[best_match_idx]
                        
                        # Print live metrics to terminal
                        print(f"🔬 Face Analyzed | Distance: {current_distance:.4f} | Time Left: {time_left:.1f}s ", end="\r")

                        if current_distance < STRICT_THRESHOLD:
                            matched_student = known_users[best_match_idx]
                            box_color = (0, 255, 0)
                            display_name = f"VERIFIED: {matched_student['name']}"
                            
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            mark_attendance(matched_student['id'], current_time)
                            
                            print(f"\n\n🎉 Welcome {matched_student['name']} ({matched_student['reg_no']})!")
                            print(f"⏱️ Attendance logged securely at: {current_time}")
                            attendance_marked = True
                            break

                # Draw targeting bounding boxes on the display frame
                cv2.rectangle(display_frame, (left, top), (right, bottom), box_color, 2)
                cv2.rectangle(display_frame, (left, bottom - 25), (right, bottom), box_color, cv2.FILLED)
                cv2.putText(display_frame, display_name, (left + 6, bottom - 6), 
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
        else:
            # If no face is in the frame, still show the countdown on screen
            cv2.putText(display_frame, f"Searching... {time_left:.1f}s", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)

        # Render display window
        cv2.imshow("BioCrypt - Scan Face", display_frame)

        if attendance_marked:
            time.sleep(2.0)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n❌ Scan session terminated manually by operator.")
            break

    # 2. Kill camera assets cleanly
    release_camera(capture)
    cv2.destroyAllWindows()

    # 3. Post-processing evaluation check
    if timeout_triggered and not attendance_marked:
        print("\n\n🛑 " + "═"*45)
        print("🛑 SECURITY TIMEOUT: IDENTITY UNVERIFIED")
        print("🛑 Biometric match could not be established within limits.")
        print("═"*45)

if __name__ == '__main__':
    mark_attendance_workflow()