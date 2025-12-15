import cv2
import os

student_name = input("Enter student name: ")
num_images = 20
save_path = f"data/enrollment/{student_name}"

os.makedirs(save_path, exist_ok=True)
cap = cv2.VideoCapture(0)

count = 0
while count < num_images:
    ret, frame = cap.read()
    cv2.imshow("Capture", frame)
   
    key = cv2.waitKey(1)
    if key & 0xFF == ord('c'):  # Press 'c' to capture
        img_name = f"{save_path}/{student_name}_{count+1}.jpg"
        cv2.imwrite(img_name, frame)
        print(f"Saved {img_name}")
        count += 1
    elif key & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()