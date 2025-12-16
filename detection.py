from ultralytics import YOLO
import cv2

class FaceDetector:
    def __init__(self, model_path="yolov8n-face.pt", conf_thresh=0.5):
        self.model = YOLO(model_path)
        self.conf_thresh = conf_thresh

    def detect_faces(self, frame):
        """
        Input: BGR frame
        Output: list of (face_crop, bbox)
        bbox = (x1, y1, x2, y2)
        """
        results = self.model(frame, conf=self.conf_thresh, verbose=False)

        faces = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                face = frame[y1:y2, x1:x2]

                if face.size == 0:
                    continue

                faces.append((face, (x1, y1, x2, y2)))

        return faces