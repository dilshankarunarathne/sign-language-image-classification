#test.py
from ultralytics import YOLO

import cv2

model = YOLO("best1.pt")

# results = model("G:/Research Documents/my data set/1-Ah/L/Ah-L-2.jpg", show=True, conf=0.3)
# cv2.waitKey(0)

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()

    if success:
        results = model(frame)

        annotated_frame = results[0].plot()

        cv2.imshow("YOLOv8 Interface", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
    else:
        break

cap.release()
cv2.destroyAllWindows()

# model.predict(source="0", show=True, conf=0.5)