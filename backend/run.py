import os
import numpy as np
import cv2
from color_correction import Main

def correct_color(input_path=None, blindness_type=None, severity=None, output_image_path=None, frame=None):
    """
    Applies color correction based on the user's chosen color blindness type and severity.
    - For images: Corrects and saves the image or returns the corrected numpy array.
    - For video frames: Corrects the frame and returns it.
    """

    if frame is not None:  
        if not isinstance(frame, np.ndarray):
            raise ValueError("Frame must be a valid numpy array.")

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame_rgb = frame_rgb.astype(np.float32) / 255.0  

        corrected_frame = Main.correctImage(
            get_path=None,
            blindness_type=blindness_type,
            severity_level=severity,
            return_type_image='np',
            frame=frame_rgb  
        )

        if corrected_frame is None or not isinstance(corrected_frame, np.ndarray):
            raise ValueError("Color correction failed, returned None.")

        corrected_frame = np.clip(corrected_frame * 255, 0, 255).astype(np.uint8)
        corrected_frame_bgr = cv2.cvtColor(corrected_frame, cv2.COLOR_RGB2BGR)
        
        return corrected_frame_bgr

    elif isinstance(input_path, str): 
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input image path '{input_path}' does not exist.")

        if output_image_path:  
            Main.correctImage(
                get_path=input_path,
                blindness_type=blindness_type,
                severity_level=severity,
                return_type_image='save', 
                save_path=output_image_path  
            )
            print(f"Image corrected and saved to {output_image_path}")
        else:
            corrected_image = Main.correctImage(
                get_path=input_path,
                blindness_type=blindness_type,
                severity_level=severity,
                return_type_image='np'
            )
            return corrected_image
    else:
        raise ValueError("Input path must be a valid file path for images or a numpy array for video frames.")
