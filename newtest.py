from ultralytics import YOLO
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Initialize YOLO model
model = YOLO("best1.pt")

# Start video capture
cap = cv2.VideoCapture(0)

# Load a font that supports Sinhala characters
sinhala_font = ImageFont.truetype("G:/SignLanguageWeb/LKLUG Regular.ttf", 20)

while True:
    success, frame = cap.read()

    if success:
        # Use YOLO to detect objects and get results
        results = model(frame)

        # Print results to understand its structure
        print(results)

        # Convert frame to PIL Image for drawing text
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)

        # Check if results is a list
        if isinstance(results, list):
            # Assuming results is a list of detections
            for detection in results:
                # Extract information from detection (adjust indices as needed)
                x1, y1, x2, y2, conf, cls = detection[:6]

                sinhala_text = "හඳුනාගත් වස්තුව"  # Replace with actual Sinhala text

                # Draw text on PIL image
                draw.text((x1, y1), sinhala_text, font=sinhala_font, fill=(255, 255, 255))

        else:
            print("Unexpected format of results object. Exiting.")
            break

        # Convert PIL Image back to OpenCV format
        annotated_frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Display the frame
        cv2.imshow("YOLOv8 Interface", annotated_frame)

        # Break the loop with 'q' key
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()