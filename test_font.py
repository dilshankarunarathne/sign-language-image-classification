# test_font.py
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def test_sinhala_font(sinhala_font_path):
    # Replace this with the actual path to your test image
    test_image_path = "G:/SignLanguageWeb/static/images/20231106_195718.jpg"

    # Open the test image
    test_image = cv2.imread(test_image_path)

    if test_image is not None:
        # Load the Sinhala font using PIL
        font = ImageFont.truetype(sinhala_font_path, 30)  # Adjust font size as needed

        # Convert OpenCV image to PIL image
        pil_image = Image.fromarray(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)

        # Draw some text using the Sinhala font
        draw.text((10, 10), "සිංහල අකුරු", font=font, fill=(255, 255, 255))

        # Convert PIL image back to OpenCV format for display
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Display the image using OpenCV
        cv2.imshow("Test Image", opencv_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"Error: Unable to read the image at {test_image_path}")

if __name__ == "__main__":
    # Replace 'IskoolaPota.ttf' with the actual path to your Sinhala font file
    sinhala_font_path = 'C:/Users/gmanu/Downloads/iskoola-pota-regular/Iskoola Pota Regular/IskoolaPota.ttf'  

    # Run the test function
    test_sinhala_font(sinhala_font_path)
