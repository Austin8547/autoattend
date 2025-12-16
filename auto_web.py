import cv2
import os
import time


# =======================
# Configuration
# =======================
CAMERA_INDEX = 0
CAPTURE_INTERVAL = 1.0  # seconds
IMAGES_PER_BATCH = 15
DISTANCES = ["CLOSE", "MID", "FAR"]
TOTAL_IMAGES = IMAGES_PER_BATCH * len(DISTANCES)
WINDOW_NAME = "Enrollment"


# =======================
# Utility Functions
# =======================
def normalize_name(name: str) -> str:
    return name.strip().replace(" ", "_").lower()


def create_save_directory(student_name: str) -> str:
    path = os.path.join("data", "enrollment", student_name)
    os.makedirs(path, exist_ok=True)
    return path


def open_camera(index: int) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam")
    return cap


def draw_ui(frame, distance: str, batch_idx: int, count: int) -> None:
    cv2.putText(frame, f"DISTANCE: {distance}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.putText(frame, f"Batch: {batch_idx + 1}/3", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.putText(frame, f"Captured: {count}/{IMAGES_PER_BATCH}", (20, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    cv2.putText(frame, "Press 'n' to move to next distance", (20, 190),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)


def save_frame(frame, save_path: str, student_name: str,
               distance: str, index: int) -> None:
    filename = f"{student_name}_{distance.lower()}_{index}.jpg"
    filepath = os.path.join(save_path, filename)
    cv2.imwrite(filepath, frame)
    print(f"[SAVED] {filepath}")


# =======================
# Main Enrollment Logic
# =======================
def run_enrollment() -> None:
    student_name = normalize_name(input("Enter student name: "))
    save_path = create_save_directory(student_name)

    cap = open_camera(CAMERA_INDEX)

    batch_idx = 0
    image_count = 0
    last_capture_time = 0.0

    print(f"[INFO] Start enrollment: {DISTANCES[batch_idx]} distance")

    try:
        while batch_idx < len(DISTANCES):
            ret, frame = cap.read()
            if not ret:
                continue

            display = frame.copy()
            now = time.time()

            # Auto-capture within batch
            if image_count < IMAGES_PER_BATCH:
                if now - last_capture_time >= CAPTURE_INTERVAL:
                    image_count += 1
                    save_frame(
                        frame,
                        save_path,
                        student_name,
                        DISTANCES[batch_idx],
                        image_count
                    )
                    last_capture_time = now

            draw_ui(
                display,
                DISTANCES[batch_idx],
                batch_idx,
                image_count
            )

            cv2.imshow(WINDOW_NAME, display)
            key = cv2.waitKey(1) & 0xFF

            # Move to next batch manually
            if image_count == IMAGES_PER_BATCH and key == ord("n"):
                batch_idx += 1
                image_count = 0
                last_capture_time = time.time()

                if batch_idx < len(DISTANCES):
                    print(f"[INFO] Switch to {DISTANCES[batch_idx]} distance")

            if key == ord("q"):
                print("[INFO] Enrollment aborted by user")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("[DONE] Enrollment finished")


# =======================
# Entry Point
# =======================
if __name__ == "__main__":
    run_enrollment()
