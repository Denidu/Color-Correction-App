import cv2
import numpy as np
from color_correction import Main  

def correct_color_realtime(blindness_type, severity):
    cap = cv2.VideoCapture(0)  

    if not cap.isOpened():
        print("Error: Could not open webcam or video file.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't read frame.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        corrected_frame = Main.correctImage(
            get_path=None,
            blindness_type=blindness_type,
            severity_level=severity,
            return_type_image='np',
            frame=frame_rgb
        )

        if corrected_frame is None or not isinstance(corrected_frame, np.ndarray):
            print("Error: Color correction failed.")
            break

        corrected_frame_bgr = cv2.cvtColor(corrected_frame, cv2.COLOR_RGB2BGR)

        combined_frame = np.hstack((frame, corrected_frame_bgr))
        cv2.imshow("Original (Left) | Corrected (Right)", combined_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

correct_color_realtime(blindness_type="Protanopia", severity="moderate")
