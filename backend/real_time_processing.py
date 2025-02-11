import cv2
import numpy as np
from utils import LoadImage
from color_correction import Main

def real_time_color_correction(color_type, severity_level):

    matrix = Main.get_color_correction_matrix(color_type, severity_level)

    cap = cv2.VideoCapture(0)  

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) / 255.0

        corrected_frame = np.dot(rgb_frame, matrix)
        corrected_frame = np.clip(corrected_frame, 0, 1) 

        corrected_frame_bgr = (corrected_frame * 255).astype(np.uint8)
        corrected_frame_bgr = cv2.cvtColor(corrected_frame_bgr, cv2.COLOR_RGB2BGR)

        cv2.imshow("Color-Corrected Video Feed", corrected_frame_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
